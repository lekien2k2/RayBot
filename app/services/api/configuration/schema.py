from typing import Optional

from pydantic import BaseModel, Field


class UpdateConfigSchema(BaseModel):
    min_distance_move: Optional[float] = None
    min_distance_lift: Optional[float] = None
    max_distance_lift: Optional[float] = None
    home_location: Optional[str] = None
    max_pwm_movement: Optional[float] = None
    max_pwm_lift: Optional[float] = None
    parameter_motor: Optional[int] = None
    home_location: Optional[str] = None


class ConfigResponeSchema(BaseModel):
    min_distance_move: float
    min_distance_lift: float
    max_distance_lift: float
    home_location: str
    max_pwm_movement: float
    max_pwm_lift: float
    parameter_motor: int
    home_location: str
