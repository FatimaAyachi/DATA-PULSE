from pathlib import Path

import pandas as pd

from data_pulse.processing.events import build_gdelt_silver


INPUT_FILE = Path(
    "data/raw/gdelt/20261006.export.CSV.zip"
)

OUTPUT_FILE = Path(
    "data/processed/events/gdelt/events_20261006.parquet"
)


def test_build_gdelt_silver(tmp_path: Path) -> None:
    output_file = tmp_path / "events.parquet"

    result = build_gdelt_silver(
        INPUT_FILE,
        output_file,
    )

    assert result.exists()

    df = pd.read_parquet(result)

    assert len(df) == 117328

    expected_columns = {
        "event_id",
        "source",
        "event_date",
        "event_code",
        "event_root_code",
        "actor1",
        "actor2",
        "action_location",
        "country_code",
        "goldstein_scale",
        "num_mentions",
        "num_sources",
        "num_articles",
        "avg_tone",
        "source_url",
    }

    assert set(df.columns) == expected_columns

    assert df["event_id"].notna().all()
    assert df["source"].eq("GDELT").all()
    assert df["event_code"].notna().all()
    assert df["source_url"].str.startswith(
    ("http://", "https://")
     ).all()