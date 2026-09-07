from collections import defaultdict


class EventBus:
    def __init__(self):
        self._handlers = defaultdict(list)

    def subscribe(self, event_name, handler):
        if not callable(handler):
            raise TypeError("Handler must be callable.")

        if handler not in self._handlers[event_name]:
            self._handlers[event_name].append(handler)

    def unsubscribe(self, event_name, handler):
        if event_name in self._handlers:
            if handler in self._handlers[event_name]:
                self._handlers[event_name].remove(handler)

    def emit(self, event_name, data=None):
        results = []

        for handler in list(self._handlers.get(event_name, [])):
            try:
                results.append({
                    "success": True,
                    "result": handler(data)
                })
            except Exception as error:
                results.append({
                    "success": False,
                    "error": str(error)
                })

        return results

    def listener_count(self, event_name):
        return len(self._handlers.get(event_name, []))

    def clear(self, event_name=None):
        if event_name is None:
            self._handlers.clear()
        else:
            self._handlers.pop(event_name, None)
