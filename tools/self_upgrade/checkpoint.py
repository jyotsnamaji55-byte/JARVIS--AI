import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def create_checkpoint(message="JARVIS pre-upgrade checkpoint"):
    try:
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )

        if status.returncode != 0:
            return {
                "success": False,
                "error": status.stderr.strip()
            }

        if status.stdout.strip():
            return {
                "success": False,
                "error": "Working tree is not clean. Upgrade checkpoint cancelled."
            }

        commit = subprocess.run(
            ["git", "commit", "--allow-empty", "-m", message],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )

        if commit.returncode != 0:
            return {
                "success": False,
                "error": commit.stderr.strip()
            }

        return {
            "success": True,
            "message": "Clean upgrade checkpoint created.",
            "output": commit.stdout.strip()
        }

    except (subprocess.SubprocessError, OSError) as error:
        return {
            "success": False,
            "error": str(error)
        }
