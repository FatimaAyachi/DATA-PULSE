from datetime import date

from pydantic import BaseModel, Field


class WaterObservation(BaseModel):
    observation_date: date
    basin: str = Field(min_length=1)
    dam: str = Field(min_length=1)
    normal_capacity_m3: float = Field(ge=0)
    reserve_m3: float = Field(ge=0)
    fill_rate: float = Field(ge=0, le=100)