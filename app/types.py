from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class CommandStatus(StrEnum):
    SUCCESS = "success"
    ERROR = "error"
    IN_PROGRESS = "in_progress"


class CommandType(StrEnum):
    GO_FORWARD = "go_forward"
    GO_BACKWARD = "go_backward"
    SCAN_QR_CODE = "scan_qr_code"
    STOP = "stop"


class MovementState(StrEnum):
    FORWARD = "go_forward"
    BACKWARD = "go_backward"
    IDLE = "idle"


@dataclass
class InboundCommand:
    id: str
    type: CommandType
    data: dict[str, Any]


@dataclass
class OutboundCommand:
    id: str
    data: dict[str, Any]
    op: str = "response"
