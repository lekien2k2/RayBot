from pydantic import Field
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel


class ReciveSchema(BaseModel):
    cmd: str
    id: str
    data: dict


class TopicEnum(StrEnum):
    status = "status"
    ram_cpu = "ram_cpu"
    command = "command"
    log = "log"
    battery = "battery"
    weight_sensor = "weight_sensor"
    forward_distance_sensor = "forward_distance_sensor"
    backward_distance_sensor = "backward_distance_sensor"
    lift_distance_sensor = "lift_distance_sensor"
    movement_motor = "movement_motor"
    movement_pwm = "movement_pwm"
    lift_motor = "lift_motor"
    lift_pwm = "lift_pwm"
    safety = "safety"
    qr_location = "qr_location"
    qr_door = "qr_door"
    door_state = "door_state"
    task = "task"

    # def __str__(self):
    #     return self.value


class OperationEnum(StrEnum):
    command = "command"
    subscribe = "subscribe"
    unsubscribe = "unsubscribe"
    publish = "publish"
    response = "response"

    # def __str__(self):
    #     return self.value


class RamCpuMsgType(BaseModel):
    ram: float
    cpu: float


class StatusMsgEnum(StrEnum):
    available = "available"
    in_progress = "in_progress"
    waiting = "waiting"
    fail = "fail"

    # def __str__(self):
    #     return self.value


class StatusMsgType(BaseModel):
    status: StatusMsgEnum


class LogMsgType(BaseModel):
    ts: int
    level: str
    file: str
    func: str
    line: int
    msg: str


class BatteryMsgType(BaseModel):
    battery: float


class WeightSensorMsgType(BaseModel):
    weight: bool


class ForwardDistanceSensorMsgType(BaseModel):
    distance: float


class BackwardDistanceSensorMsgType(BaseModel):
    distance: float


class LiftDistanceSensorMsgType(BaseModel):
    distance: float


class MovementMotorMsgType(BaseModel):
    direction: str
    speed: int


class LiftMotorMsgType(BaseModel):
    direction: str
    speed: int


class SafetyMsgType(BaseModel):
    safety: bool
    cause_by: str


class QrLocationMsgType(BaseModel):
    qr: str


class QrDoorMsgType(BaseModel):
    qr: str


class DoorStateMsgType(BaseModel):
    state: bool


class SendSchema(BaseModel):
    op: OperationEnum
    id: Optional[str] = None
    topic: Optional[TopicEnum] = None
    data: Optional[dict] = None


class CommandReciveSchema(BaseModel):
    operation: Optional[OperationEnum] = Field(..., alias="op")
    type: str
    id: str
    data: Optional[dict] = None
