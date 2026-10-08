from datetime import date

import pytest
from pydantic import ValidationError

from data_pulse.schemas.event import Event


def test_valid_event() -> None:
    event = Event(
        event_id="1326461897",
        source="GDELT",
        event_date=date(2025, 10, 6),
        event_code="051",
        event_root_code="05",
        actor1="KING",
        actor2="STUDENT",
        action_location="Pennsylvania, United States",
        country_code="US",
        goldstein_scale=3.4,
        num_mentions=10,
        num_sources=1,
        num_articles=10,
        avg_tone=5.82329317269076,
        source_url="https://example.com/article",
    )

    assert event.event_id == "1326461897"
    assert event.source == "GDELT"
    assert event.event_code == "051"
    assert event.actor1 == "KING"


def test_event_rejects_empty_event_id() -> None:
    with pytest.raises(ValidationError):
        Event(
            event_id="",
            source="GDELT",
            event_date=date(2025, 10, 6),
            event_code="051",
            event_root_code="05",
            num_mentions=10,
            num_sources=1,
            num_articles=10,
            source_url="https://example.com",
        )


def test_event_rejects_negative_mentions() -> None:
    with pytest.raises(ValidationError):
        Event(
            event_id="1326461897",
            source="GDELT",
            event_date=date(2025, 10, 6),
            event_code="051",
            event_root_code="05",
            num_mentions=-1,
            num_sources=1,
            num_articles=10,
            source_url="https://example.com",
        )