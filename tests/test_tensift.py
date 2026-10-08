from datetime import date
from pathlib import Path

from data_pulse.ingestion.tensift import load_tensift_excel


DATA_FILE = Path(
    "data/raw/morocco/data_barrages_tensift_sept_2026.xlsx"
)


def test_tensift_loads_expected_number_of_observations() -> None:
    observations = load_tensift_excel(DATA_FILE)

    assert len(observations) == 150


def test_tensift_first_observation() -> None:
    observations = load_tensift_excel(DATA_FILE)

    first = observations[0]

    assert first.observation_date == date(2026, 9, 1)
    assert first.basin == "Tensift"
    assert first.dam == "Yacoub El Mansour"
    assert first.normal_capacity_m3 == 57.45
    assert first.reserve_m3 == 49.444
    assert round(first.fill_rate, 6) == 86.064404


def test_tensift_contains_all_dams() -> None:
    observations = load_tensift_excel(DATA_FILE)

    dams = {observation.dam for observation in observations}

    assert dams == {
        "Yacoub El Mansour",
        "Lalla Takerkoust",
        "Sd Mohamed Ben Slimane El Jazouli",
        "Abou El Abess Sebti",
        "Bge My abdrhmane",
    }


def test_tensift_has_30_days() -> None:
    observations = load_tensift_excel(DATA_FILE)

    dates = {observation.observation_date for observation in observations}

    assert len(dates) == 30
    assert min(dates) == date(2026, 9, 1)
    assert max(dates) == date(2026, 9, 30)