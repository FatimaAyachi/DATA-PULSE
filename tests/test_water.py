from datetime import date

import pytest
from pydantic import ValidationError

from data_pulse.schemas.water import WaterObservation


def test_valid_water_observation() -> None:
    observation = WaterObservation(
        observation_date=date(2026, 9, 1),
        basin="Tensift",
        dam="Yacoub El Mansour",
        normal_capacity_m3=57.45,
        reserve_m3=49.444,
        fill_rate=86.064404,
    )

    assert observation.basin == "Tensift"
    assert observation.dam == "Yacoub El Mansour"
    assert observation.reserve_m3 == 49.444
    assert observation.fill_rate == 86.064404


def test_water_observation_rejects_negative_reserve() -> None:
    with pytest.raises(ValidationError):
        WaterObservation(
            observation_date=date(2026, 9, 1),
            basin="Tensift",
            dam="Yacoub El Mansour",
            normal_capacity_m3=57.45,
            reserve_m3=-1,
            fill_rate=86.0,
        )


def test_water_observation_rejects_invalid_fill_rate() -> None:
    with pytest.raises(ValidationError):
        WaterObservation(
            observation_date=date(2026, 9, 1),
            basin="Tensift",
            dam="Yacoub El Mansour",
            normal_capacity_m3=57.45,
            reserve_m3=49.444,
            fill_rate=150,
        )


def test_water_observation_rejects_empty_dam() -> None:
    with pytest.raises(ValidationError):
        WaterObservation(
            observation_date=date(2026, 9, 1),
            basin="Tensift",
            dam="",
            normal_capacity_m3=57.45,
            reserve_m3=49.444,
            fill_rate=86.0,
        )