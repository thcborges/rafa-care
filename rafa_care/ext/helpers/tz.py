from datetime import datetime, timedelta, timezone


def convert_tz(timestamp: datetime, diff: int = -3) -> datetime:
    return timestamp.astimezone(timezone(timedelta(hours=diff)))
