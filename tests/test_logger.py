import logging

from data_pulse.logging.logger import get_logger


def test_get_logger() -> None:
    logger = get_logger("test")

    assert isinstance(logger, logging.Logger)
    assert logger.name == "test"
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 1