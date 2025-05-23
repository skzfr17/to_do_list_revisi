from datetime import datetime, timezone

def get_iso_datetime_hour_minute():
    now = datetime.now(timezone.utc)
    return now.strftime('%Y-%m-%dT%H:%MZ')