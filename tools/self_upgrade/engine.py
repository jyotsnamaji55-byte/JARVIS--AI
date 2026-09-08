from tools.self_upgrade.executor import run_safe
from tools.self_upgrade.checkpoint import create_checkpoint
from tools.self_upgrade.planner import UpgradePlanner
from tools.self_upgrade.generator import generate_upgrade
from tools.self_upgrade.inspector import read_project_file
from tools.code_checker import check_python_code
from tools.self_upgrade.applier import apply_upgrade, rollback_upgrade
from tools.self_upgrade.approval import request_approval
from tools.self_upgrade.diff import create_diff


class SelfUpgradeEngine:
    def __init__(self):
        self.planner = UpgradePlanner()

    def prepare_upgrade(self, request):
        plan = self.planner.create_plan(request)

        if not plan["success"]:
            return plan

        target_file = "jarvis.py"

        inspected = read_project_file(target_file)

        if not inspected["success"]:
            return {
                "success": False,
                "stage": "inspection",
                "error": inspected["error"]
            }

        current_code = inspected["content"]

        generated = generate_upgrade(
            request,
            target_file,
            current_code
        )

        if not generated["success"]:
            return {
                "success": False,
                "stage": "generation",
                "error": generated["error"]
            }

        proposed_code = generated["code"]

        validation = check_python_code(proposed_code)

        if not validation["valid"]:
            return {
                "success": False,
                "stage": "validation",
                "error": validation["error"]
            }

        diff = create_diff(
            current_code,
            proposed_code,
            target_file
        )

        checkpoint = create_checkpoint()

        if not checkpoint["success"]:
            return {
                "success": False,
                "stage": "checkpoint",
                "error": checkpoint["error"]
            }

        return {
            "success": True,
            "stage": "preview",
            "target_file": target_file,
            "plan": plan,
            "checkpoint": checkpoint,
            "validation": validation,
            "diff": diff,
            "proposed_code": proposed_code
        }

    def apply_approved_upgrade(self, preview):
        if not preview or preview.get("stage") != "preview":
            return {
                "success": False,
                "error": "A valid upgrade preview is required."
            }

        target_file = preview.get("target_file")
        proposed_code = preview.get("proposed_code")

        if not request_approval(target_file):
            return {
                "success": False,
                "stage": "rejected",
                "message": "Upgrade cancelled by user."
            }

        applied = apply_upgrade(
            target_file,
            proposed_code
        )

        if not applied["success"]:
            return {
                "success": False,
                "stage": "apply",
                "error": applied["error"]
            }

        verification = run_safe("compile")

        if not verification["success"]:
            rollback = rollback_upgrade(target_file)

            return {
                "success": False,
                "stage": "rollback",
                "verification": verification,
                "rollback": rollback,
                "error": "Upgrade verification failed."
            }

        return {
            "success": True,
            "stage": "completed",
            "target_file": target_file,
            "apply": applied,
            "verification": verification
        }
