from unittest.mock import MagicMock

import data_pulse.pipeline as pipeline


def test_run_gdelt_pipeline(monkeypatch) -> None:
    silver_builder = MagicMock()
    quality_checker = MagicMock(return_value=[])
    spark_session = MagicMock()
    gold_builder = MagicMock()
    gold_writer = MagicMock()

    monkeypatch.setattr(
        pipeline,
        "build_gdelt_silver",
        silver_builder,
    )
    monkeypatch.setattr(
        pipeline.pd,
        "read_parquet",
        MagicMock(),
    )
    monkeypatch.setattr(
        pipeline,
        "validate_event_quality",
        quality_checker,
    )
    monkeypatch.setattr(
        pipeline,
        "create_spark_session",
        MagicMock(return_value=spark_session),
    )
    monkeypatch.setattr(
        pipeline,
        "build_gdelt_gold",
        gold_builder,
    )
    monkeypatch.setattr(
        pipeline,
        "write_gdelt_gold",
        gold_writer,
    )

    pipeline.run_gdelt_pipeline()

    silver_builder.assert_called_once_with(
        pipeline.GDELT_RAW,
        pipeline.GDELT_SILVER,
    )

    quality_checker.assert_called_once()

    gold_builder.assert_called_once_with(
        spark_session,
        pipeline.GDELT_SILVER,
    )

    gold_writer.assert_called_once_with(
        gold_builder.return_value,
        pipeline.GDELT_GOLD,
    )

    spark_session.stop.assert_called_once()