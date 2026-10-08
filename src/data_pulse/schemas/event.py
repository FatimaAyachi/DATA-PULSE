from datetime import date

from pydantic import BaseModel, Field


class Event(BaseModel):
    event_id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    event_date: date

    event_code: str = Field(min_length=1)
    event_root_code: str = Field(min_length=1)

    actor1: str | None = None
    actor2: str | None = None

    action_location: str | None = None
    country_code: str | None = None

    goldstein_scale: float | None = None
    num_mentions: int = Field(ge=0)
    num_sources: int = Field(ge=0)
    num_articles: int = Field(ge=0)
    avg_tone: float | None = None

    source_url: str = Field(min_length=1)