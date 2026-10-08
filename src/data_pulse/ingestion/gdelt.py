import csv
import zipfile
from collections.abc import Iterator
from datetime import date
from pathlib import Path

from data_pulse.schemas.event import Event


def parse_gdelt_date(value: str) -> date:
    """Convert GDELT YYYYMMDD date into a Python date."""
    return date(
        int(value[:4]),
        int(value[4:6]),
        int(value[6:8]),
    )

def parse_optional_float(value: str) -> float | None:
    """Convert an optional numeric value to float."""
    return float(value) if value else None

def iter_gdelt_events(
    file_path: str | Path,
) -> Iterator[Event]:
    """Stream GDELT events from a compressed export."""

    with zipfile.ZipFile(file_path) as archive:
        file_name = archive.namelist()[0]

        with archive.open(file_name) as file:
            reader = csv.reader(
                (
                    line.decode("utf-8", errors="replace")
                    for line in file
                ),
                delimiter="\t",
            )

            for row in reader:
                if len(row) != 58:
                    continue

                yield Event(
                    event_id=row[0],
                    source="GDELT",
                    event_date=parse_gdelt_date(row[1]),
                    event_code=row[26],
                    event_root_code=row[28],
                    actor1=row[6] or None,
                    actor2=row[16] or None,
                    action_location=row[50] or None,
                    country_code=row[51] or None,
                    goldstein_scale=parse_optional_float(row[30]),
                    num_mentions=int(row[31]),
                    num_sources=int(row[32]),
                    num_articles=int(row[33]),
                    avg_tone=parse_optional_float(row[34]),
                    source_url=row[57],
                )