from datetime import date
from pathlib import Path

import pandas as pd

from data_pulse.schemas.water import WaterObservation


DAM_COLUMNS = {
    "Yacoub El Mansour": (1, 2),
    "Lalla Takerkoust": (3, 4),
    "Sd Mohamed Ben Slimane El Jazouli": (5, 6),
    "Abou El Abess Sebti": (7, 8),
    "Bge My abdrhmane": (9, 10),
}


def load_tensift_excel(file_path: str | Path) -> list[WaterObservation]:
    """Load and normalize the Tensift dam Excel dataset."""

    df = pd.read_excel(file_path, sheet_name="Sept_2026", header=None)

    observations: list[WaterObservation] = []

    normal_capacity_row = df.iloc[1]
    data = df.iloc[3:].copy()

    for _, row in data.iterrows():
        day = int(row.iloc[0])
        observation_date = date(2026, 9, day)

        for dam, (reserve_col, fill_rate_col) in DAM_COLUMNS.items():
            observation = WaterObservation(
                observation_date=observation_date,
                basin="Tensift",
                dam=dam,
                normal_capacity_m3=float(normal_capacity_row.iloc[reserve_col]),
                reserve_m3=float(row.iloc[reserve_col]),
                fill_rate=float(row.iloc[fill_rate_col]),
            )

            observations.append(observation)

    return observations