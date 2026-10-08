from pathlib import Path

from pyspark.sql import SparkSession

from data_pulse.spark.gdelt import build_gdelt_gold


INPUT_FILE = Path(
    "data/processed/events/gdelt/events_20261006.parquet"
)


def test_build_gdelt_gold() -> None:
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

        assert gold.count() > 0

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

        assert set(gold.columns) == expected_columns

        assert (
            gold.filter(
                gold.event_count <= 0
            ).count()
            == 0
        )

        assert (
            gold.filter(
                gold.unique_event_count <= 0
            ).count()
            == 0
        )

    finally:
        spark.stop()