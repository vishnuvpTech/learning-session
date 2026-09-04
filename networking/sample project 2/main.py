from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import (
    automation_service,
    backup_service,
    command_service,
    models,
    schemas,
    troubleshoot_service,
)
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Network Automation & Troubleshooting Platform",
    description=(
        "Module 1: Device Inventory | Module 2: Connectivity | Module 3/4: Command "
        "Execution | Module 5: Backup | Module 6: Automation | Module 7: "
        "Troubleshooting | Module 8: Audit"
    ),
    version="1.0.0",
)


@app.get("/", tags=["meta"])
def root():
    return {"message": "Network Automation & Troubleshooting Platform API", "docs": "/docs"}


def _get_device_or_404(device_id: int, db: Session) -> models.Device:
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")
    return device


# ---------------------------------------------------------------------------
# Module 1 — Device Inventory
# ---------------------------------------------------------------------------

@app.post("/devices", response_model=schemas.DeviceOut, status_code=201, tags=["1. inventory"])
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Device).filter(models.Device.ip == device.ip).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"A device with IP {device.ip} already exists.")

    db_device = models.Device(
        hostname=device.hostname,
        ip=device.ip,
        vendor=device.vendor,
        device_type=device.device_type,
        username=device.username,
        password=device.password,
        status="never_contacted",
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


@app.get("/devices", response_model=List[schemas.DeviceOut], tags=["1. inventory"])
def list_devices(db: Session = Depends(get_db)):
    return db.query(models.Device).all()


@app.delete("/devices/{device_id}", status_code=204, tags=["1. inventory"])
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device = _get_device_or_404(device_id, db)
    db.delete(device)
    db.commit()
    return None


# ---------------------------------------------------------------------------
# Module 2 — Device Connectivity
# ---------------------------------------------------------------------------

@app.post("/devices/{device_id}/connect", response_model=schemas.ConnectResult, tags=["2. connectivity"])
def connect_device(device_id: int, db: Session = Depends(get_db)):
    device = _get_device_or_404(device_id, db)
    return command_service.connect_device(db, device)


# ---------------------------------------------------------------------------
# Module 3 — Command Execution (single device)
# ---------------------------------------------------------------------------

@app.post("/devices/{device_id}/command", response_model=schemas.CommandResult, tags=["3. command execution"])
def run_command(device_id: int, req: schemas.CommandRequest, db: Session = Depends(get_db)):
    device = _get_device_or_404(device_id, db)
    return command_service.run_command(device, req.command, req.is_config)


# ---------------------------------------------------------------------------
# Module 4 — Bulk Command Execution
# ---------------------------------------------------------------------------

@app.post("/devices/bulk-command", response_model=schemas.BulkCommandResult, tags=["4. bulk command"])
def bulk_command(req: schemas.BulkCommandRequest, db: Session = Depends(get_db)):
    if req.all:
        devices = db.query(models.Device).all()
    elif req.device_ids:
        devices = db.query(models.Device).filter(models.Device.id.in_(req.device_ids)).all()
    else:
        raise HTTPException(status_code=400, detail="Provide device_ids or set all=true.")

    if not devices:
        raise HTTPException(status_code=404, detail="No matching devices found.")

    results = command_service.run_bulk_command(devices, req.command, req.is_config)
    success = sum(1 for r in results if r["success"])
    return {
        "total": len(results),
        "success": success,
        "failed": len(results) - success,
        "results": results,
    }


# ---------------------------------------------------------------------------
# Module 5 — Configuration Backup
# ---------------------------------------------------------------------------

@app.post("/backup/{device_id}", response_model=schemas.BackupResult, tags=["5. backup"])
def backup_device(device_id: int, db: Session = Depends(get_db)):
    device = _get_device_or_404(device_id, db)
    return backup_service.backup_single_device(db, device)


@app.post("/backup/all", response_model=schemas.BackupAllResult, tags=["5. backup"])
def backup_all(db: Session = Depends(get_db)):
    devices = db.query(models.Device).all()
    results = backup_service.backup_all_devices(db, devices)
    success = sum(1 for r in results if r["status"] == "success")
    return {
        "total": len(results),
        "success": success,
        "failed": len(results) - success,
        "results": results,
    }


@app.get("/backups", response_model=List[schemas.BackupRecord], tags=["5. backup"])
def get_backups():
    return backup_service.list_backups()


# ---------------------------------------------------------------------------
# Module 6 — Automation
# ---------------------------------------------------------------------------

def _run_automation(action: str, device_ids: List[int], db: Session, apply_fn, req) -> dict:
    devices = db.query(models.Device).filter(models.Device.id.in_(device_ids)).all()
    if not devices:
        raise HTTPException(status_code=404, detail="No matching devices found for given device_ids.")

    results = [apply_fn(db, device, req) for device in devices]
    success = sum(1 for r in results if r["result"] == "success")
    rolled_back = sum(1 for r in results if r["result"] == "rolled_back")
    failed = sum(1 for r in results if r["result"] == "failed")

    return {
        "action": action,
        "total": len(results),
        "success": success,
        "rolled_back": rolled_back,
        "failed": failed,
        "results": results,
    }


@app.post("/automation/vlan", response_model=schemas.AutomationResponse, tags=["6. automation"])
def automation_vlan(req: schemas.VlanAutomationRequest, db: Session = Depends(get_db)):
    return _run_automation("vlan", req.device_ids, db, automation_service.apply_vlan, req)


@app.post("/automation/ospf", response_model=schemas.AutomationResponse, tags=["6. automation"])
def automation_ospf(req: schemas.OspfAutomationRequest, db: Session = Depends(get_db)):
    return _run_automation("ospf", req.device_ids, db, automation_service.apply_ospf, req)


@app.post("/automation/bgp", response_model=schemas.AutomationResponse, tags=["6. automation"])
def automation_bgp(req: schemas.BgpAutomationRequest, db: Session = Depends(get_db)):
    return _run_automation("bgp", req.device_ids, db, automation_service.apply_bgp, req)


# ---------------------------------------------------------------------------
# Module 7 — Troubleshooting
# ---------------------------------------------------------------------------

@app.post("/troubleshoot", response_model=schemas.TroubleshootResponse, tags=["7. troubleshoot"])
def troubleshoot(req: schemas.TroubleshootRequest, db: Session = Depends(get_db)):
    source_device = db.query(models.Device).filter(models.Device.ip == req.source).first()
    if not source_device:
        raise HTTPException(
            status_code=404,
            detail=f"Source device {req.source} not found in inventory. Register it via POST /devices first.",
        )
    return troubleshoot_service.run_troubleshoot(source_device, req.destination, req.port)


# ---------------------------------------------------------------------------
# Module 8 — Audit
# ---------------------------------------------------------------------------

@app.get("/audit", response_model=List[schemas.AuditLogOut], tags=["8. audit"])
def get_audit(db: Session = Depends(get_db)):
    return db.query(models.AuditLog).order_by(models.AuditLog.timestamp.desc()).all()
