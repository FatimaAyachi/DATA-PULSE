from pathlib import Path

import pandas as pd

from data_pulse.ingestion.tensift import load_tensift_excel


def build_water_silver(
    input_path: str | Path,
    output_path: str | Path,
) -> Path:
    """Transform raw Tensift water data into a Silver Parquet dataset."""

    observations = load_tensift_excel(input_path)

    df = pd.DataFrame(
        [
            {
                "observation_date": observation.observation_date,
                "basin": observation.basin,
                "dam": observation.dam,
                "normal_capacity_m3": observation.normal_capacity_m3,
                "reserve_m3": observation.reserve_m3,
                "fill_rate": observation.fill_rate,
            }
            for observation in observations
        ]
    )

    df = df.sort_values(
        ["observation_date", "dam"]
    ).reset_index(drop=True)

    df["observation_date"] = pd.to_datetime(
        df["observation_date"]
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        output_path,
        engine="pyarrow",
        index=False,
    )

    return output_path