from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ALLOWED_EXTENSIONS = {".py"}
IGNORED_DIRS = {
    ".git",
    "venv",
    "__pycache__",
    "coding_workspace",
    "core/agent_backup_30",
}

IGNORED_FILE_PREFIXES = (
    "jarvis_backup",
    "jarvis_before_",
)


def list_python_files():
    files = []

    for path in PROJECT_ROOT.rglob("*.py"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.name.startswith(IGNORED_FILE_PREFIXES):
            continue
        files.append(str(path.relative_to(PROJECT_ROOT)))

    return sorted(files)


def read_project_file(relative_path):
    path = (PROJECT_ROOT / relative_path).resolve()

    try:
        path.relative_to(PROJECT_ROOT)
    except ValueError:
        return {
            "success": False,
            "error": "Access outside JARVIS project is not allowed."
        }

    if path.suffix not in ALLOWED_EXTENSIONS:
        return {
            "success": False,
            "error": "Only Python files can be inspected."
        }

    if not path.exists() or not path.is_file():
        return {
            "success": False,
            "error": "File not found."
        }

    try:
        return {
            "success": True,
            "file": str(path.relative_to(PROJECT_ROOT)),
            "content": path.read_text(encoding="utf-8")
        }
    except OSError as error:
        return {
            "success": False,
            "error": str(error)
        }
