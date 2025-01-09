from typing import Optional

from pydantic import BaseModel, Field


# class UpdateConfigSchema(BaseModel):
#     min_distance_move: Optional[float] = Field(..., description="Min distance move")
#     min_distance_lift: Optional[float] = Field(..., description="Min distance lift")
#     max_distance_lift: Optional[float] = Field(..., description="Max distance lift")
#     home_location: Optional[str] = Field(..., description="Home location")
#     max_pwm_movement: Optional[float] = Field(..., description="Max pwm movement")
#     max_pwm_lift: Optional[float] = Field(..., description="Max pwm lift")
#     parameter_motor: Optional[int] = Field(..., description="Parameter motor")
#     home_location: Optional[str] = Field(..., description="Home location")


# class ConfigResponeSchema(BaseModel):
#     min_distance_move: float
#     min_distance_lift: float
#     max_distance_lift: float
#     home_location: str
#     max_pwm_movement: float
#     max_pwm_lift: float
#     parameter_motor: int
#     home_location: str
