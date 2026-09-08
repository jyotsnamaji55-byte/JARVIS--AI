import difflib


def create_diff(old_code, new_code, file_path):
    diff = difflib.unified_diff(
        old_code.splitlines(),
        new_code.splitlines(),
        fromfile=f"{file_path} (current)",
        tofile=f"{file_path} (proposed)",
        lineterm=""
    )

    return "\n".join(diff)
