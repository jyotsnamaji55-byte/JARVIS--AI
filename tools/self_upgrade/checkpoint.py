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

        subprocess.run(
            ["git", "add", "-A"],
            cwd=PROJECT_ROOT,
            check=True,
            timeout=30
        )

        commit = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )

        if commit.returncode not in (0, 1):
            return {
                "success": False,
                "error": commit.stderr.strip()
            }

        return {
            "success": True,
            "message": "Upgrade checkpoint created.",
            "output": commit.stdout.strip()
        }

    except (subprocess.SubprocessError, OSError) as error:
        return {
            "success": False,
            "error": str(error)
        }
