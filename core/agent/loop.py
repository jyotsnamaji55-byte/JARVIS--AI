from core.agent.recovery import RecoveryEngine
from core.agent.verifier import ResultVerifier


class AgenticLoop:
    def __init__(self, controller, max_iterations=3):
        self.controller = controller
        self.max_iterations = max_iterations
        self.recovery = RecoveryEngine(max_retries=2)
        self.verifier = ResultVerifier()

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

            verification = self.verifier.verify(result)

            history.append({
                "iteration": iteration,
                "success": result["success"],
                "verified": verification["verified"],
                "verification": verification,
                "result": result
            })

            if verification["verified"]:
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
            "error": "Agentic workflow failed verification."
        }
