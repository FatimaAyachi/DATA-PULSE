from data_pulse.config import settings


def test_settings() -> None:
    assert settings.app_name == "DATA-PULSE"
    assert settings.environment == "development"
    assert settings.log_level == "INFO"