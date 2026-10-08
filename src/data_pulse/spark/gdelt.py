from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


def build_gdelt_gold(
    spark: SparkSession,
    input_path: str | Path,
) -> DataFrame:
    """Build daily GDELT event aggregates using Spark."""

    df = spark.read.parquet(str(input_path))

    gold = (
        df.groupBy("event_date")
        .agg(
            F.count("*").alias("event_count"),
            F.countDistinct("event_id").alias("unique_event_count"),
            F.sum("num_mentions").alias("total_mentions"),
            F.sum("num_sources").alias("total_sources"),
            F.sum("num_articles").alias("total_articles"),
            F.avg("goldstein_scale").alias("avg_goldstein_scale"),
            F.avg("avg_tone").alias("avg_tone"),
        )
        .orderBy("event_date")
    )

    return gold