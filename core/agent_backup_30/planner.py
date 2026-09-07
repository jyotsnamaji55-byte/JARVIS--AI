class AgentPlanner:
    def create_plan(self, goal):
        goal = goal.strip()

        if not goal:
            return []

        return [
            {
                "step": 1,
                "action": "analyze_goal",
                "description": f"Analyze the goal: {goal}"
            },
            {
                "step": 2,
                "action": "select_tools",
                "description": "Select the required tools."
            },
            {
                "step": 3,
                "action": "execute",
                "description": "Execute the required tool actions."
            },
            {
                "step": 4,
                "action": "verify",
                "description": "Verify the result."
            }
        ]
