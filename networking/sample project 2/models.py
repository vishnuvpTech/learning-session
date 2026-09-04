from sqlalchemy import Column, DateTime, Integer, String, Text
from .database import Base


class Device(Base):
    """A network device tracked by the automation platform."""

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, nullable=False, index=True)
    ip = Column(String, nullable=False, unique=True, index=True)
    vendor = Column(String, nullable=False)          # e.g. "cisco", "arista", "juniper"
    device_type = Column(String, nullable=False)     # Netmiko device_type, e.g. "cisco_ios"
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)         # NOTE: plaintext for demo simplicity, see README
    last_backup = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default="never_contacted")


class AuditLog(Base):
    """
    Module 8 — Audit trail.

    Records every configuration-affecting action: who requested it, what
    the action was, when it happened, which device it touched, the
    configuration before and after, and the final result.
    """

    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    requested_by = Column(String, nullable=False)          # WHO
    action = Column(String, nullable=False)                # WHAT (e.g. "automation.vlan", "command.config")
    device_hostname = Column(String, nullable=False)       # WHICH DEVICE
    old_config = Column(Text, nullable=True)                # OLD CONFIGURATION
    new_config = Column(Text, nullable=True)                # NEW CONFIGURATION
    result = Column(String, nullable=False)                 # success / rolled_back / failed
    detail = Column(Text, nullable=True)
