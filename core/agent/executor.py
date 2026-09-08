class AgentExecutor:
    def execute(self, tool_name, arguments, registry):
        tool = registry.get(tool_name)

        if not tool:
            return {
                "success": False,
                "tool": tool_name,
                "error": f"Tool not found: {tool_name}"
            }

        try:
            result = tool["function"](*arguments)

            if isinstance(result, dict) and "success" in result:
                return {
                    "success": result["success"],
                    "tool": tool_name,
                    "result": result,
                    "error": result.get("error")
                }

            return {
                "success": True,
                "tool": tool_name,
                "result": result
            }

        except Exception as error:
            return {
                "success": False,
                "tool": tool_name,
                "error": str(error)
            }
