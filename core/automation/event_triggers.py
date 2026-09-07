from core.events.bus import EventBus


class EventTriggerBridge:
    def __init__(self, trigger_engine):
        self.trigger_engine = trigger_engine
        self.event_bus = EventBus()
        self._event_map = {}

    def register(
        self,
        event_name,
        trigger_name,
        condition,
        action
    ):
        if not event_name.strip():
            raise ValueError("Event name cannot be empty.")

        if not trigger_name.strip():
            raise ValueError("Trigger name cannot be empty.")

        self.trigger_engine.register(
            trigger_name,
            condition,
            action,
            event_name=event_name
        )

        def handler(data):
            context = {
                "event": event_name,
                "data": data
            }

            trigger = self.trigger_engine.triggers.get(
                trigger_name
            )

            if not trigger:
                return {
                    "success": False,
                    "trigger": trigger_name,
                    "error": "Trigger not found."
                }

            executed = trigger.check_and_run(context)

            return {
                "success": executed,
                "trigger": trigger_name,
                "event": event_name
            }

        self.event_bus.subscribe(
            event_name,
            handler
        )

        self._event_map.setdefault(
            event_name,
            []
        ).append(trigger_name)

    def emit(self, event_name, data=None):
        return self.event_bus.emit(
            event_name,
            data
        )

    def listener_count(self, event_name):
        return self.event_bus.listener_count(
            event_name
        )

    def remove_event(self, event_name):
        trigger_names = self._event_map.pop(
            event_name,
            []
        )

        self.event_bus.clear(event_name)

        for trigger_name in trigger_names:
            self.trigger_engine.remove(
                trigger_name
            )

        return trigger_names

    def list_event_bindings(self):
        return {
            event: list(triggers)
            for event, triggers in self._event_map.items()
        }
