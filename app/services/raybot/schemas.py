from dataclasses import dataclass
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel


class ReciveDataSchema(BaseModel):
    forward_distance: Optional[float] = None
    backward_distance: Optional[float] = None
    lift_distance: Optional[float] = None
    weight: Optional[float] = None
    battery: Optional[float] = None
    movement_motor: Optional[int] = None
    movement_pwm: Optional[float] = None
    lift_motor: Optional[int] = None
    lift_pwm: Optional[float] = None
    safety: Optional[bool] = None
    door_state: Optional[bool] = None
    min_distance_move: Optional[float] = None
    min_distance_lift: Optional[float] = None
    max_distance_lift: Optional[float] = None
    max_pwm_movement: Optional[float] = None
    max_pwm_lift: Optional[float] = None
    

class RayBotInfoSchema(BaseModel):
    current_cmd: str
    forward_distance: float
    backward_distance: float
    lift_distance: float
    weight: float
    battery: float
    movement_motor: int
    movement_pwm: float
    min_distance_move: float
    min_distance_lift: float
    max_distance_lift: float
    max_pwm_movement: float
    max_pwm_lift: float
    lift_motor: int
    lift_pwm: float
    safety: bool
    door_state: bool
    qr_location: str
    qr_door: str
    home_location: str

    # Định nghĩa property qr_location
    @property
    def qr_location(self):
        return self._qr_location

    @qr_location.setter
    def qr_location(self, value):
        self._qr_location = value


class RaybotConfigSchema(BaseModel):
    min_distance_move: float
    max_distance_move: float
    min_distance_lift: float
    max_distance_lift: float
    home_location: str
    max_pwm_movement: float
    max_pwm_lift: float
    parameter_motor: int
    home_location: str


class CommandEnum(StrEnum):
    forward = "forward"
    backward = "backward"
    stop = "stop"
    drop_box = "drop_box"
    lift_box = "lift_box"
    open_box = "open_box"
    close_box = "close_box"
    get_data = "get_data"

    # def __str__(self):
    #     return self.value


class DataCommandEnum(StrEnum):
    pwm: str = "pwm"
    distance: str = "distance"
    weight: str = "weight"

    # def __str__(self):
    #     return self.value


class CommandActionEnum(StrEnum):
    move_forward = "handle_move_forward"
    move_backward = "handle_move_backward"
    move_to_location = "handle_move_to_location"
    drop_box = "handle_drop_box"
    lift_box = "handle_lift_box"
    open_box = "handle_open_box"
    close_box = "handle_close_box"
    stop = "handle_stop"
    scan_location = "handle_scan_location"
    check_qr = "handle_check_qr"
    wait_get_item = "handle_wait_get_item"

    blink_led = "handle_blink_led"

    # def __str__(self):
    #     return self.value


@dataclass
class SendToRayBotSchema:
    command: CommandEnum
    data: Optional[DataCommandEnum] = None


class RobotStatusEnum(StrEnum):
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    LOW_BATTERY = "low_battery"
    CHARGING = "charging"

    # def __str__(self):
    #     return self.value
