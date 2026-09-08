import ast
import operator


_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate(node):
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp):
        operation = _ALLOWED_OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Operator is not allowed.")

        left = _evaluate(node.left)
        right = _evaluate(node.right)

        if isinstance(node.op, ast.Pow):
            if abs(right) > 100:
                raise ValueError("Exponent is too large.")

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        operation = _ALLOWED_OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unary operator is not allowed.")

        return operation(_evaluate(node.operand))

    raise ValueError("Only basic arithmetic expressions are allowed.")


def calculate(expression):
    expression = expression.strip()

    if not expression:
        return {
            "success": False,
            "error": "Expression is empty."
        }

    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree)

        return {
            "success": True,
            "expression": expression,
            "result": result
        }

    except (SyntaxError, ValueError, ZeroDivisionError, OverflowError) as error:
        return {
            "success": False,
            "error": str(error)
        }
