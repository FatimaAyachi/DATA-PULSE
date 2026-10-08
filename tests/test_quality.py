import pandas as pd

from data_pulse.quality import validate_event_quality


def test_valid_events_pass_quality_checks() -> None:
    df = pd.DataFrame(
        {
            "event_id": ["1", "2"],
            "event_date": ["2026-10-05", "2026-10-06"],
            "num_mentions": [10, 20],
            "num_sources": [1, 2],
            "num_articles": [10, 20],
        }
    )

    df["event_date"] = pd.to_datetime(df["event_date"])

    errors = validate_event_quality(df)

    assert errors == []


def test_duplicate_event_ids_are_detected() -> None:
    df = pd.DataFrame(
        {
            "event_id": ["1", "1"],
            "event_date": ["2026-10-05", "2026-10-06"],
            "num_mentions": [10, 20],
            "num_sources": [1, 2],
            "num_articles": [10, 20],
        }
    )

    df["event_date"] = pd.to_datetime(df["event_date"])

    errors = validate_event_quality(df)

    assert "event_id contains duplicates" in errors


def test_negative_metrics_are_detected() -> None:
    df = pd.DataFrame(
        {
            "event_id": ["1"],
            "event_date": ["2026-10-05"],
            "num_mentions": [-1],
            "num_sources": [-2],
            "num_articles": [-3],
        }
    )

    df["event_date"] = pd.to_datetime(df["event_date"])

    errors = validate_event_quality(df)

    assert "num_mentions contains negative values" in errors
    assert "num_sources contains negative values" in errors
    assert "num_articles contains negative values" in errors


def test_future_dates_are_detected() -> None:
    df = pd.DataFrame(
        {
            "event_id": ["1"],
            "event_date": ["2099-01-01"],
            "num_mentions": [10],
            "num_sources": [1],
            "num_articles": [10],
        }
    )

    df["event_date"] = pd.to_datetime(df["event_date"])

    errors = validate_event_quality(df)

    assert "event_date contains future dates" in errors