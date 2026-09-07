class AgenticLoop:
    def __init__(self, controller, max_iterations=3):
        self.controller = controller
        self.max_iterations = max_iterations

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

        return {
            "success": False,
            "iterations": self.max_iterations,
            "history": history,
            "error": "Maximum agent iterations reached."
        }
