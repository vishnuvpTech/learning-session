from sqlalchemy import Column, Integer, String, DateTime
from .database import Base


class Device(Base):
    """A network device tracked by the backup system."""

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, nullable=False, index=True)
    ip = Column(String, nullable=False, unique=True, index=True)
    vendor = Column(String, nullable=False)          # e.g. "cisco", "arista", "juniper"
    device_type = Column(String, nullable=False)     # Netmiko device_type, e.g. "cisco_ios"
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)         # NOTE: plaintext for demo simplicity, see README
    last_backup = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default="never_backed_up")
