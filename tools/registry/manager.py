class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name, description, function):
        self._tools[name] = {
            "name": name,
            "description": description,
            "function": function
        }

    def get(self, name):
        return self._tools.get(name)

    def list_tools(self):
        return list(self._tools.values())

    def has(self, name):
        return name in self._tools
