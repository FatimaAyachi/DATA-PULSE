from datetime import datetime

import pytest
from pydantic import ValidationError

from data_pulse.schemas.event import Event


def test_valid_event() -> None:
    event = Event(
        event_id="event-001",
        source="api",
        title="Test event",
        timestamp=datetime(2026, 10, 7, 20, 0, 0),
        category="test",
        value=42.5,
    )

    assert event.event_id == "event-001"
    assert event.source == "api"
    assert event.title == "Test event"
    assert event.category == "test"
    assert event.value == 42.5


def test_event_without_optional_value() -> None:
    event = Event(
        event_id="event-002",
        source="api",
        title="Test event",
        timestamp=datetime(2026, 10, 7, 20, 0, 0),
        category="test",
    )

    assert event.value is None


def test_event_rejects_empty_event_id() -> None:
    with pytest.raises(ValidationError):
        Event(
            event_id="",
            source="api",
            title="Test event",
            timestamp=datetime(2026, 10, 7, 20, 0, 0),
            category="test",
        )


def test_event_rejects_empty_source() -> None:
    with pytest.raises(ValidationError):
        Event(
            event_id="event-003",
            source="",
            title="Test event",
            timestamp=datetime(2026, 10, 7, 20, 0, 0),
            category="test",
        )


def test_event_rejects_empty_title() -> None:
    with pytest.raises(ValidationError):
        Event(
            event_id="event-004",
            source="api",
            title="",
            timestamp=datetime(2026, 10, 7, 20, 0, 0),
            category="test",
        )


def test_event_rejects_empty_category() -> None:
    with pytest.raises(ValidationError):
        Event(
            event_id="event-005",
            source="api",
            title="Test event",
            timestamp=datetime(2026, 10, 7, 20, 0, 0),
            category="",
        )
def test_event_from_dict() -> None:
    data = {
        "event_id": "event-006",
        "source": "api",
        "title": "External event",
        "timestamp": "2026-10-07T20:00:00",
        "category": "external",
        "value": 15.5,
    }

    event = Event.model_validate(data)

    assert event.event_id == "event-006"
    assert event.title == "External event"
    assert event.timestamp.year == 2026
    assert event.value == 15.5
def test_event_from_invalid_dict() -> None:
    data = {
        "event_id": "",
        "source": "api",
        "title": "Invalid event",
        "timestamp": "not-a-date",
        "category": "test",
    }

    with pytest.raises(ValidationError):
        Event.model_validate(data)