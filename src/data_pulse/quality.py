
import pandas as pd


def validate_event_quality(df: pd.DataFrame) -> list[str]:
    """Validate core quality rules for GDELT event data."""

    errors: list[str] = []

    if df["event_id"].duplicated().any():
        errors.append("event_id contains duplicates")

    if (df["num_mentions"] < 0).any():
        errors.append("num_mentions contains negative values")

    if (df["num_sources"] < 0).any():
        errors.append("num_sources contains negative values")

    if (df["num_articles"] < 0).any():
        errors.append("num_articles contains negative values")

    event_dates = pd.to_datetime(df["event_date"])

    if (event_dates > pd.Timestamp.today().normalize()).any():
        errors.append("event_date contains future dates")

    return errors