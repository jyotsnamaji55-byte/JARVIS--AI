from core.agent.recovery import RecoveryEngine


class AgenticLoop:
    def __init__(self, controller, max_iterations=3):
        self.controller = controller
        self.max_iterations = max_iterations
        self.recovery = RecoveryEngine(max_retries=2)

    def run(self, goal):
        goal = goal.strip()

        if not goal:
            return {
                "success": False,
                "error": "Empty goal."
            }

        history = []

        for iteration in range(1, self.max_iterations + 1):
            result = self.controller.execute_goal(goal)

            history.append({
                "iteration": iteration,
                "success": result["success"],
                "result": result
            })

            if result["success"]:
                return {
                    "success": True,
                    "iterations": iteration,
                    "history": history
                }

            if not self.recovery.should_retry(
                result,
                iteration
            ):
                break

        return {
            "success": False,
            "iterations": len(history),
            "history": history,
            "error": "Agentic workflow failed after recovery attempts."
        }
