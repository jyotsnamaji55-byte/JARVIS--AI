from core.automation.queue import TaskQueue
from core.automation.scheduler import Scheduler
from core.automation.recurring import RecurringScheduler
from core.automation.triggers import TriggerEngine
from core.automation.event_triggers import EventTriggerBridge


class AutomationManager:
    def __init__(self):
        self.queue = TaskQueue()
        self.scheduler = Scheduler()
        self.recurring = RecurringScheduler()
        self.triggers = TriggerEngine()
        self.events = EventTriggerBridge(self.triggers)

    def add_task(self, task):
        self.queue.add(task)

    def get_next_task(self):
        return self.queue.next()

    def schedule_once(self, name, delay_seconds, action):
        self.scheduler.schedule_once(name, delay_seconds, action)

    def schedule_recurring(self, name, interval_seconds, action):
        return self.recurring.add(
            name,
            interval_seconds,
            action
        )

    def register_trigger(
        self,
        name,
        condition,
        action,
        event_name="manual",
        enabled=True
    ):
        self.triggers.register(
            name,
            condition,
            action,
            event_name=event_name,
            enabled=enabled
        )

    def remove_trigger(self, name):
        self.triggers.remove(name)

    def enable_trigger(self, name):
        self.triggers.enable(name)

    def disable_trigger(self, name):
        self.triggers.disable(name)

    def register_event_trigger(
        self,
        event_name,
        trigger_name,
        condition,
        action
    ):
        self.events.register(
            event_name,
            trigger_name,
            condition,
            action
        )

    def emit_event(self, event_name, data=None):
        return self.events.emit(
            event_name,
            data
        )

    def remove_event(self, event_name):
        return self.events.remove_event(event_name)

    def run_pending(self, context=None):
        self.scheduler.run_pending()

        recurring_executed = self.recurring.run_pending()

        trigger_context = {
            "data": context
        }

        trigger_executed = self.triggers.check_all(
            trigger_context
        )

        return {
            "recurring_executed": recurring_executed,
            "triggers_executed": trigger_executed
        }

    def queue_size(self):
        return self.queue.size()

    def active_recurring_tasks(self):
        return self.recurring.active_count()

    def list_triggers(self):
        return self.triggers.list_triggers()

    def persistent_triggers(self):
        return self.triggers.persistent_triggers()

    def list_event_bindings(self):
        return self.events.list_event_bindings()
