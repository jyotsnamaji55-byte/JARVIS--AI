from core.agent.workflow import WorkflowManager


class AgentOrchestrator:
    def __init__(self, controller, automation):
        self.controller = controller
        self.automation = automation
        self.workflow = WorkflowManager()

    def run_goal(self, goal):
        goal = goal.strip()

        if not goal:
            return {
                "success": False,
                "error": "Empty goal."
            }

        self.workflow.save(
            goal,
            "executing",
            1,
            1
        )

        try:
            result = self.controller.execute_goal(goal)

            if result["success"]:
                self.workflow.save(
                    goal,
                    "completed",
                    1,
                    5,
                    result
                )
            else:
                self.workflow.save(
                    goal,
                    "paused",
                    1,
                    4,
                    result
                )

            return result

        except Exception as error:
            self.workflow.save(
                goal,
                "paused",
                1,
                4,
                {"error": str(error)}
            )

            return {
                "success": False,
                "error": str(error)
            }

    def run_pending_automation(self):
        return self.automation.run_pending()

    def current_workflow(self):
        return self.workflow.load()
