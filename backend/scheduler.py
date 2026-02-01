import time
from datetime import datetime

from db import get_settings, get_last_sent_date, update_last_sent_date
from report_generator import generate_daily_report
from notifiers.email_sender import send_email
from notifiers.report_formatter import format_report_text


def scheduler_loop():
    print("Scheduler started")

    while True:
        try:
            settings = get_settings()

            report_time = settings["report_time"]  # "HH:MM"
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            today = now.strftime("%Y-%m-%d")

            last_sent = get_last_sent_date()
            print("Now:", current_time,
            "Target:", report_time,
            "Last sent:", last_sent)

            if current_time >= report_time and last_sent != today:
                report = generate_daily_report(today)

                # For now: just log
                print("=== DAILY REPORT ===")
                print(report)
                print("====================")

                if settings["enable_email"] and settings["email"]:
                    body = format_report_text(report)
                    send_email(
                        settings["email"],
                        f"SkillTrace Daily Report - {today}",
                        body
                    )

                update_last_sent_date(today)

        except Exception as e:
            print("Scheduler error:", e)

        time.sleep(30)


def generate_and_send_once():
    settings = get_settings()
    today = datetime.now().strftime("%Y-%m-%d")
    report = generate_daily_report(today)

    if settings["enable_email"] and settings["email"]:
        body = format_report_text(report)
        send_email(
            settings["email"],
            f"SkillTrace Daily Report - {today}",
            body
        )
