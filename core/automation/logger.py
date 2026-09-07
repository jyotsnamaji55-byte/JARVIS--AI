from datetime import datetime
from pathlib import Path


LOG_PATH = Path("logs/jarvis.log")


def log_event(event, details=""):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().isoformat()

    with LOG_PATH.open("a", encoding="utf-8") as log:
        log.write(f"[{timestamp}] {event} {details}\n")
