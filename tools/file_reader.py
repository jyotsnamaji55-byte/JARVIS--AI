from pathlib import Path


WORKSPACE = Path("tools/coding_workspace").resolve()


def read_file(filename):
    path = (WORKSPACE / filename).resolve()

    if WORKSPACE not in path.parents:
        return "ERROR: Access outside coding workspace is not allowed."

    if not path.exists():
        return f"ERROR: File '{filename}' not found."

    if not path.is_file():
        return f"ERROR: '{filename}' is not a file."

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return "ERROR: File is not a UTF-8 text file."
    except OSError as error:
        return f"ERROR: Could not read file: {error}"
