from pathlib import Path

from pyspark.sql import SparkSession

from data_pulse.spark.gdelt import (
    build_gdelt_gold,
    write_gdelt_gold,
)

INPUT_FILE = Path(
    "data/processed/events/gdelt/events_20261006.parquet"
)

OUTPUT_DIR = Path(
    "data/processed/events/gdelt/gold/test_daily_event_metrics"
)


def test_build_and_write_gdelt_gold() -> None:
    spark = (
        SparkSession.builder
        .appName("DATA-PULSE-test")
        .master("local[2]")
        .config("spark.driver.memory", "2g")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    try:
        gold = build_gdelt_gold(
            spark,
            INPUT_FILE,
        )

        output_path = write_gdelt_gold(
            gold,
            OUTPUT_DIR,
        )

        assert output_path.exists()

        reloaded = spark.read.parquet(str(output_path))

        assert reloaded.count() > 0

        expected_columns = {
            "event_date",
            "event_count",
            "unique_event_count",
            "total_mentions",
            "total_sources",
            "total_articles",
            "avg_goldstein_scale",
            "avg_tone",
        }

        assert set(reloaded.columns) == expected_columns

        assert (
            reloaded.filter(
                reloaded.event_count <= 0
            ).count()
            == 0
        )

    finally:
        spark.stop()