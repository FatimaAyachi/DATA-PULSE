from datetime import datetime

from pydantic import BaseModel, Field


class Event(BaseModel):
    event_id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    title: str = Field(min_length=1)
    timestamp: datetime
    category: str = Field(min_length=1)
    value: float | None = None