from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from data_pulse.ingestion.gdelt import iter_gdelt_events


BATCH_SIZE = 5_000


def build_gdelt_silver(
    input_path: str | Path,
    output_path: str | Path,
) -> Path:
    """Transform GDELT events into a Silver Parquet dataset."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    writer = None
    batch = []

    try:
        for event in iter_gdelt_events(input_path):
            batch.append(event.model_dump())

            if len(batch) >= BATCH_SIZE:
                table = pa.Table.from_pylist(batch)

                if writer is None:
                    writer = pq.ParquetWriter(
                        output_path,
                        table.schema,
                    )

                writer.write_table(table)
                batch.clear()

        if batch:
            table = pa.Table.from_pylist(batch)

            if writer is None:
                writer = pq.ParquetWriter(
                    output_path,
                    table.schema,
                )

            writer.write_table(table)

    finally:
        if writer is not None:
            writer.close()

    return output_path