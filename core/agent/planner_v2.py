class DynamicPlanner:
    def create_plan(self, goal):
        goal = goal.strip()

        if not goal:
            return []

        steps = [
            {
                "step": 1,
                "action": "understand",
                "description": "Understand the user's goal."
            },
            {
                "step": 2,
                "action": "plan",
                "description": "Break the goal into executable steps."
            },
            {
                "step": 3,
                "action": "select_tools",
                "description": "Select the most suitable available tools."
            },
            {
                "step": 4,
                "action": "execute",
                "description": "Execute the planned actions."
            },
            {
                "step": 5,
                "action": "verify",
                "description": "Verify the result."
            }
        ]

        return steps
