from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Module 1 — Device Inventory
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Module 2 — Device Connectivity
# ---------------------------------------------------------------------------

class ConnectResult(BaseModel):
    device_id: int
    hostname: str
    reachable: bool
    detail: str
    device_prompt: Optional[str] = None


# ---------------------------------------------------------------------------
# Module 3 / 4 — Command Execution (single + bulk)
# ---------------------------------------------------------------------------

class CommandRequest(BaseModel):
    command: str = Field(..., examples=["show ip interface brief"])
    is_config: bool = Field(
        False, description="True if this is a configuration command rather than a show/exec command."
    )


class CommandResult(BaseModel):
    device_id: int
    hostname: str
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None


class BulkCommandRequest(BaseModel):
    device_ids: Optional[List[int]] = Field(
        None, description="Specific device IDs to target. Omit (or leave null) together with all=True to target every device."
    )
    all: bool = Field(False, description="If true, run against every device in inventory.")
    command: str
    is_config: bool = False


class BulkCommandResult(BaseModel):
    total: int
    success: int
    failed: int
    results: List[CommandResult]


# ---------------------------------------------------------------------------
# Module 5 — Configuration Backup
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Module 6 — Automation (VLAN / OSPF / BGP)
# ---------------------------------------------------------------------------

class VlanAutomationRequest(BaseModel):
    device_ids: List[int]
    vlan_id: int = Field(..., examples=[100])
    vlan_name: str = Field(..., examples=["AUTOMATION"])
    requested_by: str = Field("anonymous", description="Who is requesting this change (for the audit log).")


class OspfNetwork(BaseModel):
    network: str = Field(..., examples=["10.10.10.0"])
    wildcard: str = Field(..., examples=["0.0.0.255"])


class OspfAutomationRequest(BaseModel):
    device_ids: List[int]
    process_id: int = Field(..., examples=[1])
    area: int = Field(0, examples=[0])
    networks: List[OspfNetwork]
    requested_by: str = "anonymous"


class BgpNeighbor(BaseModel):
    ip: str
    remote_asn: int


class BgpAutomationRequest(BaseModel):
    device_ids: List[int]
    local_asn: int
    neighbors: List[BgpNeighbor]
    requested_by: str = "anonymous"


class AutomationStepResult(BaseModel):
    device_id: int
    hostname: str
    stage_reached: str  # validate / pre_check / configure / post_check / success / rollback
    result: str          # success / rolled_back / failed
    detail: str


class AutomationResponse(BaseModel):
    action: str
    total: int
    success: int
    rolled_back: int
    failed: int
    results: List[AutomationStepResult]


# ---------------------------------------------------------------------------
# Module 7 — Troubleshooting
# ---------------------------------------------------------------------------

class TroubleshootRequest(BaseModel):
    source: str = Field(..., description="IP of the source device, must already be registered in inventory.")
    destination: str
    port: int


class TroubleshootStep(BaseModel):
    step: str
    passed: bool
    detail: str


class TroubleshootResponse(BaseModel):
    connectivity: bool
    failed_at: Optional[str] = None
    port: int
    recommendation: str
    steps: List[TroubleshootStep]


# ---------------------------------------------------------------------------
# Module 8 — Audit
# ---------------------------------------------------------------------------

class AuditLogOut(BaseModel):
    id: int
    timestamp: datetime
    requested_by: str
    action: str
    device_hostname: str
    old_config: Optional[str] = None
    new_config: Optional[str] = None
    result: str
    detail: Optional[str] = None

    class Config:
        from_attributes = True
