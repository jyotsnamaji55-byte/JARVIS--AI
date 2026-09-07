import json
from datetime import datetime
from pathlib import Path


STATE_PATH = Path("data/agent/workflow_state.json")


class WorkflowManager:
    def __init__(self):
        STATE_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def save(self, goal, status, iteration, step, data=None):
        state = {
            "goal": goal,
            "status": status,
            "iteration": iteration,
            "step": step,
            "data": data,
            "updated_at": datetime.now().isoformat()
        }

        STATE_PATH.write_text(
            json.dumps(state, indent=2),
            encoding="utf-8"
        )

    def load(self):
        if not STATE_PATH.exists():
            return None

        try:
            return json.loads(
                STATE_PATH.read_text(
                    encoding="utf-8"
                )
            )
        except (OSError, json.JSONDecodeError):
            return None

    def clear(self):
        if STATE_PATH.exists():
            STATE_PATH.unlink()

    def has_active_workflow(self):
        state = self.load()

        if not state:
            return False

        return state.get("status") in {
            "planning",
            "executing",
            "recovering",
            "paused"
        }
