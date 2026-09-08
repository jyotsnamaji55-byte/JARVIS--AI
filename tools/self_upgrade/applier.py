from pathlib import Path
import shutil

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKUP_DIR = PROJECT_ROOT / "data" / "agent" / "upgrade_backups"


def apply_upgrade(relative_path, new_code):
    path = (PROJECT_ROOT / relative_path).resolve()

    try:
        path.relative_to(PROJECT_ROOT)
    except ValueError:
        return {
            "success": False,
            "error": "Access outside JARVIS project is not allowed."
        }

    if path.suffix != ".py":
        return {
            "success": False,
            "error": "Only Python files can be upgraded."
        }

    if not path.exists() or not path.is_file():
        return {
            "success": False,
            "error": "Target file not found."
        }

    if not isinstance(new_code, str) or not new_code.strip():
        return {
            "success": False,
            "error": "New code is empty."
        }

    try:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

        backup_path = BACKUP_DIR / f"{path.name}.backup"
        shutil.copy2(path, backup_path)

        path.write_text(new_code, encoding="utf-8")

        return {
            "success": True,
            "file": relative_path,
            "backup": str(backup_path.relative_to(PROJECT_ROOT)),
            "message": "Upgrade applied successfully."
        }

    except OSError as error:
        return {
            "success": False,
            "error": str(error)
        }


def rollback_upgrade(relative_path):
    path = (PROJECT_ROOT / relative_path).resolve()

    try:
        path.relative_to(PROJECT_ROOT)
    except ValueError:
        return {
            "success": False,
            "error": "Access outside JARVIS project is not allowed."
        }

    backup_path = BACKUP_DIR / f"{path.name}.backup"

    if not backup_path.exists():
        return {
            "success": False,
            "error": "Backup not found."
        }

    try:
        shutil.copy2(backup_path, path)

        return {
            "success": True,
            "file": relative_path,
            "message": "Previous version restored successfully."
        }

    except OSError as error:
        return {
            "success": False,
            "error": str(error)
        }
