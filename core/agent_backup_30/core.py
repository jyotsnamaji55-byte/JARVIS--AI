from core.agent.planner import AgentPlanner
from core.agent.tool_selector import ToolSelector
from core.agent.executor import AgentExecutor


class AgentCore:
    def __init__(self, registry):
        self.registry = registry
        self.planner = AgentPlanner()
        self.selector = ToolSelector()
        self.executor = AgentExecutor()

    def run(self, goal):
        plan = self.planner.create_plan(goal)

        if not plan:
            return {
                "success": False,
                "error": "Empty goal."
            }

        tools = self.selector.select(goal, self.registry)

        if not tools:
            return {
                "success": False,
                "error": "No suitable tool found."
            }

        results = []

        for tool_name in tools:
            if tool_name == "generate_code":
                execution = self.executor.execute(
                    tool_name,
                    (goal,),
                    self.registry
                )
            else:
                execution = {
                    "success": False,
                    "tool": tool_name,
                    "error": "Automatic arguments are not implemented yet."
                }

            results.append(execution)

        return {
            "success": all(item["success"] for item in results),
            "plan": plan,
            "tools": tools,
            "results": results
        }
