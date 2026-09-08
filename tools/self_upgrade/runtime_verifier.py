import ast


def verify_python_runtime(code):
    try:
        tree = ast.parse(code)

        names = {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name)
        }

        if "ast" in names:
            ast.parse("import ast")

        compile(tree, "<upgrade>", "exec")

        return {
            "valid": True,
            "error": None
        }

    except (SyntaxError, NameError, AttributeError, TypeError, ValueError) as error:
        return {
            "valid": False,
            "error": str(error)
        }
