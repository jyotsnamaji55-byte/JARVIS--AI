import ast

FORBIDDEN_IMPORTS = {
    "subprocess",
    "shutil",
    "socket",
    "ctypes",
    "telnetlib",
}

FORBIDDEN_CALLS = {
    "eval",
    "exec",
    "__import__",
}

FORBIDDEN_ATTRIBUTES = {
    "system",
    "popen",
    "run",
    "Popen",
    "check_output",
    "check_call",
}


def verify_python_runtime(code):
    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".")[0]
                    if root in FORBIDDEN_IMPORTS:
                        return {
                            "valid": False,
                            "error": f"Forbidden import detected: {root}"
                        }

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    root = node.module.split(".")[0]
                    if root in FORBIDDEN_IMPORTS:
                        return {
                            "valid": False,
                            "error": f"Forbidden import detected: {root}"
                        }

            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in FORBIDDEN_CALLS:
                        return {
                            "valid": False,
                            "error": f"Forbidden call detected: {node.func.id}"
                        }

                elif isinstance(node.func, ast.Attribute):
                    if node.func.attr in FORBIDDEN_ATTRIBUTES:
                        return {
                            "valid": False,
                            "error": f"Forbidden attribute call detected: {node.func.attr}"
                        }

            elif isinstance(node, ast.Attribute):
                if node.attr in FORBIDDEN_ATTRIBUTES:
                    return {
                        "valid": False,
                        "error": f"Forbidden attribute detected: {node.attr}"
                    }

        compile(tree, "<upgrade>", "exec")

        return {
            "valid": True,
            "error": None
        }

    except (SyntaxError, TypeError, ValueError) as error:
        return {
            "valid": False,
            "error": str(error)
        }
