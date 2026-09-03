from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import backup_service, models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Network Configuration Backup System",
    description=(
        "FastAPI -> Device Inventory -> Nornir -> Netmiko -> Network Devices.\n\n"
        "Register devices, back them up individually or all at once (in parallel "
        "via Nornir), and review saved backups."
    ),
    version="1.0.0",
)


@app.get("/", tags=["meta"])
def root():
    return {"message": "Network Configuration Backup System API", "docs": "/docs"}


# ---------------------------------------------------------------------------
# Device inventory
# ---------------------------------------------------------------------------

@app.post("/devices", response_model=schemas.DeviceOut, status_code=201, tags=["devices"])
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    """Register a new device in the inventory."""
    existing = db.query(models.Device).filter(models.Device.ip == device.ip).first()
    if existing:
        raise HTTPException(
            status_code=400, detail=f"A device with IP {device.ip} already exists."
        )

    db_device = models.Device(
        hostname=device.hostname,
        ip=device.ip,
        vendor=device.vendor,
        device_type=device.device_type,
        username=device.username,
        password=device.password,
        status="never_backed_up",
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


@app.get("/devices", response_model=List[schemas.DeviceOut], tags=["devices"])
def list_devices(db: Session = Depends(get_db)):
    """List every device in the inventory."""
    return db.query(models.Device).all()


@app.get("/devices/{device_id}", response_model=schemas.DeviceOut, tags=["devices"])
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")
    return device


@app.delete("/devices/{device_id}", status_code=204, tags=["devices"])
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")
    db.delete(device)
    db.commit()
    return None


# ---------------------------------------------------------------------------
# Backups
# ---------------------------------------------------------------------------

@app.post(
    "/devices/{device_id}/backup",
    response_model=schemas.BackupResult,
    tags=["backup"],
)
def backup_device(device_id: int, db: Session = Depends(get_db)):
    """Back up a single device via a direct Netmiko connection."""
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")

    return backup_service.backup_single_device(db, device)


@app.post("/backup/all", response_model=schemas.BackupAllResult, tags=["backup"])
def backup_all(db: Session = Depends(get_db)):
    """Back up every device in the inventory in parallel, via Nornir + Netmiko."""
    devices = db.query(models.Device).all()
    results = backup_service.backup_all_devices(db, devices)

    success = sum(1 for r in results if r["status"] == "success")
    failed = len(results) - success

    return {
        "total": len(results),
        "success": success,
        "failed": failed,
        "results": results,
    }


@app.get("/backups", response_model=List[schemas.BackupRecord], tags=["backup"])
def get_backups():
    """List every backup file that has been saved to disk."""
    return backup_service.list_backups()
