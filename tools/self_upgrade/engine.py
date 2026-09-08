from tools.self_upgrade.executor import run_safe
from tools.self_upgrade.checkpoint import create_checkpoint
from tools.self_upgrade.planner import UpgradePlanner


class SelfUpgradeEngine:
    def __init__(self):
        self.planner = UpgradePlanner()

    def prepare_upgrade(self, request):
        plan = self.planner.create_plan(request)

        if not plan["success"]:
            return plan

        checkpoint = create_checkpoint()

        if not checkpoint["success"]:
            return {
                "success": False,
                "stage": "checkpoint",
                "error": checkpoint["error"]
            }

        verification = run_safe("compile")

        if not verification["success"]:
            return {
                "success": False,
                "stage": "verification",
                "error": verification["error"]
            }

        return {
            "success": True,
            "stage": "ready",
            "plan": plan,
            "checkpoint": checkpoint,
            "verification": verification
        }
