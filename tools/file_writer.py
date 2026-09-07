from pathlib import Path


WORKSPACE = Path("tools/coding_workspace").resolve()


def write_file(filename, content, overwrite=False):
    path = (WORKSPACE / filename).resolve()

    if WORKSPACE not in path.parents:
        return "ERROR: Access outside coding workspace is not allowed."

    if path.exists() and path.is_dir():
        return f"ERROR: '{filename}' is a directory."

    if path.exists() and not overwrite:
        return (
            f"ERROR: File '{filename}' already exists. "
            "Set overwrite=True to replace it."
        )

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"File written successfully: {filename}"
    except OSError as error:
        return f"ERROR: Could not write file: {error}"
