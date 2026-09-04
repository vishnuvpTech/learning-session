"""Module 8 — Audit trail helper. Every config-affecting action calls log_audit()."""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from . import models


def log_audit(
    db: Session,
    requested_by: str,
    action: str,
    device_hostname: str,
    result: str,
    old_config: str = None,
    new_config: str = None,
    detail: str = None,
) -> models.AuditLog:
    entry = models.AuditLog(
        timestamp=datetime.now(timezone.utc),
        requested_by=requested_by,
        action=action,
        device_hostname=device_hostname,
        old_config=old_config,
        new_config=new_config,
        result=result,
        detail=detail,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
