from pathlib import Path

import pandas as pd
from pyspark.sql import SparkSession

from data_pulse.logging.logger import get_logger
from data_pulse.processing.events import build_gdelt_silver
from data_pulse.quality import validate_event_quality
from data_pulse.spark.gdelt import build_gdelt_gold, write_gdelt_gold

logger = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

GDELT_RAW = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "gdelt"
    / "20261006.export.CSV.zip"
)

GDELT_SILVER = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "events"
    / "gdelt"
    / "events_20261006.parquet"
)

GDELT_GOLD = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "events"
    / "gdelt"
    / "gold"
    / "daily_event_metrics"
)


def create_spark_session() -> SparkSession:
    """Create the Spark session used by DATA-PULSE."""

    return (
        SparkSession.builder
        .appName("DATA-PULSE-pipeline")
        .master("local[2]")
        .config("spark.driver.memory", "2g")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )


def run_gdelt_pipeline() -> None:
    """Run the complete GDELT data pipeline."""

    logger.info("Starting DATA-PULSE GDELT pipeline")

    logger.info("Building Silver dataset")
    build_gdelt_silver(
        GDELT_RAW,
        GDELT_SILVER,
    )

    logger.info("Running data quality checks")
    silver_df = pd.read_parquet(GDELT_SILVER)
    errors = validate_event_quality(silver_df)

    if errors:
        raise ValueError(
            "Data quality validation failed: "
            + "; ".join(errors)
        )

    logger.info("Data quality validation passed")

    spark = create_spark_session()
    spark.sparkContext.setLogLevel("ERROR")

    try:
        logger.info("Building Gold dataset")
        gold_df = build_gdelt_gold(
            spark,
            GDELT_SILVER,
        )

        logger.info("Writing Gold dataset")
        write_gdelt_gold(
            gold_df,
            GDELT_GOLD,
        )

    finally:
        spark.stop()

    logger.info("DATA-PULSE GDELT pipeline completed successfully")


if __name__ == "__main__":
    run_gdelt_pipeline()