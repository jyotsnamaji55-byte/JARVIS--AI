from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ALLOWED_COMMANDS = {
    "compile": ["python", "-m", "compileall", "-q", "core", "tools", "jarvis.py"],
    "git_status": ["git", "status", "--short"],
}

def run_safe(command_name):
    if command_name not in ALLOWED_COMMANDS:
        return {
            "success": False,
            "error": "Command is not allowed."
        }

    try:
        result = subprocess.run(
            ALLOWED_COMMANDS[command_name],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=60
        )

        return {
            "success": result.returncode == 0,
            "command": command_name,
            "output": result.stdout.strip(),
            "error": result.stderr.strip()
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "command": command_name,
            "error": "Command timed out."
        }

    except OSError as error:
        return {
            "success": False,
            "command": command_name,
            "error": str(error)
        }
