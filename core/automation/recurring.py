from datetime import datetime, timedelta


class RecurringTask:
    def __init__(self, name, interval_seconds, action):
        self.name = name
        self.interval_seconds = interval_seconds
        self.action = action
        self.next_run = datetime.now() + timedelta(seconds=interval_seconds)
        self.status = "scheduled"

    def run_if_due(self):
        if self.status != "scheduled":
            return False

        if datetime.now() < self.next_run:
            return False

        try:
            self.action()
            self.next_run = datetime.now() + timedelta(
                seconds=self.interval_seconds
            )
            return True
        except Exception:
            self.status = "failed"
            return False


class RecurringScheduler:
    def __init__(self):
        self.tasks = []

    def add(self, name, interval_seconds, action):
        task = RecurringTask(
            name,
            interval_seconds,
            action
        )
        self.tasks.append(task)
        return task

    def run_pending(self):
        executed = 0

        for task in self.tasks:
            if task.run_if_due():
                executed += 1

        return executed

    def active_count(self):
        return sum(
            1 for task in self.tasks
            if task.status == "scheduled"
        )
