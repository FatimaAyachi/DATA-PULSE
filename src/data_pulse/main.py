from data_pulse.logging.logger import get_logger

logger = get_logger(__name__)


def main() -> None:
    logger.info("DATA-PULSE application started")
    logger.info("Environment initialized successfully")


if __name__ == "__main__":
    main()