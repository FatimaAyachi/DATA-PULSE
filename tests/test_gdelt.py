from datetime import date
from pathlib import Path

from data_pulse.ingestion.gdelt import iter_gdelt_events


DATA_FILE = Path(
    "data/raw/gdelt/20261006.export.CSV.zip"
)


def test_gdelt_first_event() -> None:
    event = next(iter_gdelt_events(DATA_FILE))

    assert event.event_id == "1326461897"
    assert event.source == "GDELT"
    assert event.event_date == date(2025, 10, 6)
    assert event.event_code == "051"
    assert event.event_root_code == "05"
    assert event.actor1 == "KING"
    assert event.actor2 == "STUDENT"
    assert event.country_code == "US"
    assert event.goldstein_scale == 3.4
    assert event.num_mentions == 10
    assert event.num_sources == 1
    assert event.num_articles == 10


def test_gdelt_first_event_has_source_url() -> None:
    event = next(iter_gdelt_events(DATA_FILE))

    assert event.source_url.startswith("https://")


def test_gdelt_event_count() -> None:
    events = iter_gdelt_events(DATA_FILE)

    count = sum(1 for _ in events)

    assert count == 117328