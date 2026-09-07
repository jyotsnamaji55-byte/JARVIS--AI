from core.agent.planner_v2 import DynamicPlanner
from core.agent.tool_selector import ToolSelector
from core.agent.executor import AgentExecutor
from core.agent.state import AgentState


class AgentCore:
    def __init__(self, registry):
        self.registry = registry
        self.planner = DynamicPlanner()
        self.selector = ToolSelector()
        self.executor = AgentExecutor()
        self.state = AgentState()

    def run(self, goal):
        goal = goal.strip()

        if not goal:
            return {
                "success": False,
                "error": "Empty goal."
            }

        self.state.save(
            goal,
            "planning",
            0
        )

        plan = self.planner.create_plan(goal)

        if not plan:
            self.state.save(goal, "failed", 0)
            return {
                "success": False,
                "error": "Could not create a plan."
            }

        self.state.save(
            goal,
            "selecting_tools",
            2
        )

        tools = self.selector.select(
            goal,
            self.registry
        )

        if not tools:
            self.state.save(
                goal,
                "waiting_for_tool",
                2
            )

            return {
                "success": False,
                "error": "No suitable tool found.",
                "plan": plan,
                "tools": []
            }

        results = []

        for index, tool_name in enumerate(tools, start=1):
            self.state.save(
                goal,
                "executing",
                index + 2
            )

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

            if not execution["success"]:
                self.state.save(
                    goal,
                    "failed",
                    index + 2,
                    execution.get("error")
                )

                return {
                    "success": False,
                    "plan": plan,
                    "tools": tools,
                    "results": results
                }

        self.state.save(
            goal,
            "completed",
            len(plan)
        )

        return {
            "success": True,
            "plan": plan,
            "tools": tools,
            "results": results
        }
