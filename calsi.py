"""Simple command-line calculator.

Run:  python calculator.py
Type an expression like 12 * (3 + 4) and press Enter. Type q to quit.
"""

import ast
import operator

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluate(node):
    """Safely evaluate a parsed arithmetic expression (no eval())."""
    if isinstance(node, ast.Expression):
        return evaluate(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](evaluate(node.left), evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](evaluate(node.operand))
    raise ValueError("Unsupported expression")


def calculate(text):
    tree = ast.parse(text, mode="eval")
    return evaluate(tree)


def main():
    print("Calculator - supports + - * / // % ** and parentheses. Type q to quit.")
    while True:
        text = input("> ").strip()
        if text.lower() in ("q", "quit", "exit"):
            break
        if not text:
            continue
        try:
            result = calculate(text)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            print(result)
        except ZeroDivisionError:
            print("Error: cannot divide by zero")
        except (ValueError, SyntaxError, OverflowError):
            print("Error: invalid expression")


if __name__ == "__main__":
    main()


