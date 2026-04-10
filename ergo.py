"""
Ergo - Automated ergonomic break reminder.

Reads ergo-config.json from the same directory, then fires an OS
notification on the configured interval during working hours.
Clicking the notification opens the exercise page in the browser.
"""

import json
import sys
import time
import webbrowser
from datetime import datetime
from pathlib import Path

import schedule
from plyer import notification

CONFIG_FILE = Path(__file__).parent / "ergo-config.json"

DEFAULTS = {
    "break_interval_minutes": 60,
    "break_duration_seconds": 30,
    "start_hour": 9,
    "end_hour": 18,
    "exercise_page_url": "",
}


def load_config():
    if not CONFIG_FILE.exists():
        print(f"[Ergo] Config file not found at {CONFIG_FILE}. Using defaults.")
        return dict(DEFAULTS)
    try:
        with CONFIG_FILE.open() as f:
            data = json.load(f)
        config = {**DEFAULTS, **data}
        return config
    except json.JSONDecodeError as e:
        print(f"[Ergo] Config file is invalid JSON: {e}. Using defaults.")
        return dict(DEFAULTS)


def within_working_hours(start_hour, end_hour):
    now = datetime.now().hour
    return start_hour <= now < end_hour


def fire_break(config):
    if not within_working_hours(config["start_hour"], config["end_hour"]):
        return

    url = config["exercise_page_url"]

    notification.notify(
        title="Ergo Break",
        message="Time for your ergonomic break!",
        app_name="Ergo",
        timeout=10,
    )

    # Open the exercise page immediately
    if url and not url.startswith("https://<"):
        webbrowser.open(url)


def main():
    config = load_config()
    interval = config["break_interval_minutes"]

    print(f"[Ergo] Starting. Break every {interval} min, "
          f"working hours {config['start_hour']}:00–{config['end_hour']}:00.")

    schedule.every(interval).minutes.do(fire_break, config=config)

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[Ergo] Stopped.")
        sys.exit(0)
