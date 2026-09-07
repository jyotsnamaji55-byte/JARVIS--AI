import json
from pathlib import Path
from datetime import datetime

STATE_PATH = Path("data/agent/agent_state.json")


class AgentState:
    def __init__(self):
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

    def save(self, goal, status, step=0, result=None):
        state = {
            "goal": goal,
            "status": status,
            "step": step,
            "result": result,
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
                STATE_PATH.read_text(encoding="utf-8")
            )
        except Exception:
            return None

    def clear(self):
        if STATE_PATH.exists():
            STATE_PATH.unlink()
