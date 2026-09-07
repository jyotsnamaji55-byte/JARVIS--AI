import time
from datetime import datetime, timedelta


class Scheduler:
    def __init__(self):
        self.tasks = []

    def schedule_once(self, name, delay_seconds, action):
        run_at = datetime.now() + timedelta(seconds=delay_seconds)

        self.tasks.append({
            "name": name,
            "run_at": run_at,
            "action": action,
            "status": "scheduled"
        })

    def run_pending(self):
        now = datetime.now()

        for task in self.tasks:
            if task["status"] != "scheduled":
                continue

            if now >= task["run_at"]:
                try:
                    task["action"]()
                    task["status"] = "completed"
                except Exception:
                    task["status"] = "failed"

    def pending_count(self):
        return sum(
            1 for task in self.tasks
            if task["status"] == "scheduled"
        )
