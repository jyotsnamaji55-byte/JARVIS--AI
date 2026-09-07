from core.agent.core import AgentCore
from core.automation.manager import AutomationManager


class AgenticController:
    def __init__(self, registry):
        self.agent = AgentCore(registry)
        self.automation = AutomationManager()

    def execute_goal(self, goal):
        goal = goal.strip()

        if not goal:
            return {
                "success": False,
                "error": "Empty goal."
            }

        result = self.agent.run(goal)

        return {
            "success": result["success"],
            "goal": goal,
            "agent": result,
            "automation": {
                "queue_size": self.automation.queue_size(),
                "active_recurring_tasks":
                    self.automation.active_recurring_tasks(),
                "triggers":
                    self.automation.list_triggers()
            }
        }

    def register_trigger(self, name, condition, action):
        self.automation.register_trigger(
            name,
            condition,
            action
        )

    def remove_trigger(self, name):
        self.automation.remove_trigger(name)

    def run_automation(self, context=None):
        return self.automation.run_pending(
            context
        )
