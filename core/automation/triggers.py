from datetime import datetime
from core.automation.trigger_store import TriggerStore


class Trigger:
    def __init__(self, name, condition, action, enabled=True):
        self.name = name
        self.condition = condition
        self.action = action
        self.enabled = enabled
        self.last_run = None

    def check_and_run(self, context=None):
        if not self.enabled:
            return False

        try:
            if not self.condition(context):
                return False

            self.action(context)
            self.last_run = datetime.now().isoformat()
            return True

        except Exception:
            return False


class TriggerEngine:
    def __init__(self):
        self.triggers = {}
        self.store = TriggerStore()

    def register(
        self,
        name,
        condition,
        action,
        event_name="manual",
        enabled=True
    ):
        trigger = Trigger(
            name,
            condition,
            action,
            enabled
        )

        self.triggers[name] = trigger

        self.store.save(
            name,
            event_name,
            enabled
        )

    def remove(self, name):
        self.triggers.pop(name, None)
        self.store.delete(name)

    def enable(self, name):
        if name in self.triggers:
            self.triggers[name].enabled = True

        self.store.set_enabled(name, True)

    def disable(self, name):
        if name in self.triggers:
            self.triggers[name].enabled = False

        self.store.set_enabled(name, False)

    def check_all(self, context=None):
        executed = []

        for name, trigger in self.triggers.items():
            if trigger.check_and_run(context):
                executed.append(name)

        return executed

    def list_triggers(self):
        return [
            {
                "name": trigger.name,
                "enabled": trigger.enabled,
                "last_run": trigger.last_run
            }
            for trigger in self.triggers.values()
        ]

    def persistent_triggers(self):
        return self.store.list_all()

    def has_trigger(self, name):
        return name in self.triggers

    def trigger_count(self):
        return len(self.triggers)
