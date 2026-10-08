from pathlib import Path

import pandas as pd

from data_pulse.processing.water import build_water_silver


INPUT_FILE = Path(
    "data/raw/morocco/data_barrages_tensift_sept_2026.xlsx"
)

OUTPUT_FILE = Path(
    "data/processed/water/tensift/test_water_observations.parquet"
)


def test_build_water_silver_creates_parquet() -> None:
    output = build_water_silver(INPUT_FILE, OUTPUT_FILE)

    assert output.exists()


def test_build_water_silver_has_expected_shape() -> None:
    build_water_silver(INPUT_FILE, OUTPUT_FILE)

    df = pd.read_parquet(OUTPUT_FILE)

    assert df.shape == (150, 6)


def test_build_water_silver_has_expected_columns() -> None:
    build_water_silver(INPUT_FILE, OUTPUT_FILE)

    df = pd.read_parquet(OUTPUT_FILE)

    assert list(df.columns) == [
        "observation_date",
        "basin",
        "dam",
        "normal_capacity_m3",
        "reserve_m3",
        "fill_rate",
    ]


def test_build_water_silver_has_no_missing_values() -> None:
    build_water_silver(INPUT_FILE, OUTPUT_FILE)

    df = pd.read_parquet(OUTPUT_FILE)

    assert not df.isna().any().any()


def test_build_water_silver_has_valid_fill_rates() -> None:
    build_water_silver(INPUT_FILE, OUTPUT_FILE)

    df = pd.read_parquet(OUTPUT_FILE)

    assert df["fill_rate"].between(0, 100).all()