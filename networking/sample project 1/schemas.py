from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class DeviceCreate(BaseModel):
    hostname: str = Field(..., examples=["router1"])
    ip: str = Field(..., examples=["192.168.10.1"])
    vendor: str = Field(..., examples=["cisco"])
    device_type: str = Field(..., examples=["cisco_ios"], description="Netmiko device_type string")
    username: str
    password: str


class DeviceOut(BaseModel):
    id: int
    hostname: str
    ip: str
    vendor: str
    device_type: str
    last_backup: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True


class BackupResult(BaseModel):
    device_id: int
    hostname: str
    status: str  # "success" | "failed"
    message: str
    backup_file: Optional[str] = None


class BackupAllResult(BaseModel):
    total: int
    success: int
    failed: int
    results: List[BackupResult]


class BackupRecord(BaseModel):
    hostname: str
    filename: str
    timestamp: datetime
    size_bytes: int
