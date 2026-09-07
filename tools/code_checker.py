import ast


def check_python_code(code):
    try:
        ast.parse(code)
        return {
            "valid": True,
            "error": None
        }
    except SyntaxError as error:
        return {
            "valid": False,
            "error": f"SyntaxError: {error.msg} at line {error.lineno}"
        }
