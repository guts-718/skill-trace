from datetime import datetime, timezone

from db import (
    get_total_time_between,
    get_category_breakdown,
    get_top_domains,
    get_session_count
)


def generate_daily_report(date_str: str):
    """
    date_str format: YYYY-MM-DD
    """

    date = datetime.strptime(date_str, "%Y-%m-%d")

    start = datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        tzinfo=timezone.utc
    )

    end = start.replace(hour=23, minute=59, second=59)

    start_ts = int(start.timestamp())
    end_ts = int(end.timestamp())

    report = {
        "date": date_str,
        "total_time_sec": get_total_time_between(start_ts, end_ts),
        "category_breakdown": get_category_breakdown(start_ts, end_ts),
        "top_domains": get_top_domains(start_ts, end_ts, limit=5),
        "session_count": get_session_count(start_ts, end_ts)
    }

    return report
