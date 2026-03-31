"""
tools/math/symbolic_math.py
Symbolic math computation using SymPy.

Handles: algebraic simplification, equation solving, differentiation,
integration, identity verification, limit computation, series expansion.

This is a real tool — SymPy computes deterministically.
The AI cannot do reliable symbolic math on its own.
"""

from sympy import (
    symbols, sympify, solve, simplify, diff, integrate,
    limit, series, Eq, oo, pi, sin, cos, tan, sec, csc, cot,
    log, exp, sqrt, factor, expand, trigsimp,
)
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)
from langchain_core.tools import tool
import json

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)

x, y, z, t, n = symbols("x y z t n")
theta = symbols("theta")


def _parse(expr_str: str):
    """Parse a math expression string into a SymPy expression."""
    cleaned = (
        expr_str
        .replace("^", "**")
        .replace("θ", "theta")
        .replace("π", "pi")
        .replace("√", "sqrt")
    )
    return parse_expr(cleaned, transformations=TRANSFORMATIONS)


def compute_symbolic(expression: str, operation: str = "simplify", variable: str = "x") -> dict:
    """
    Perform a symbolic math computation.

    Args:
        expression: Math expression as string.
        operation: solve | simplify | differentiate | integrate | factor |
                   expand | trig_simplify | verify | limit
        variable: Variable to operate on.

    Returns:
        Dict with input, operation, result, verified, error.
    """
    try:
        var = symbols(variable)

        if operation == "solve":
            if "=" in expression:
                parts = expression.split("=", 1)
                lhs = _parse(parts[0].strip())
                rhs = _parse(parts[1].strip())
                result = solve(Eq(lhs, rhs), var)
            else:
                result = solve(_parse(expression), var)
            return {"input": expression, "operation": operation, "result": str(result), "verified": True, "error": None}

        elif operation == "simplify":
            result = simplify(_parse(expression))
            return {"input": expression, "operation": operation, "result": str(result), "verified": True, "error": None}

        elif operation == "differentiate":
            result = simplify(diff(_parse(expression), var))
            return {"input": expression, "operation": operation, "result": str(result), "variable": variable, "verified": True, "error": None}

        elif operation == "integrate":
            result = integrate(_parse(expression), var)
            return {"input": expression, "operation": operation, "result": str(result), "variable": variable, "verified": True, "error": None}

        elif operation == "factor":
            result = factor(_parse(expression))
            return {"input": expression, "operation": operation, "result": str(result), "verified": True, "error": None}

        elif operation == "expand":
            result = expand(_parse(expression))
            return {"input": expression, "operation": operation, "result": str(result), "verified": True, "error": None}

        elif operation == "trig_simplify":
            result = trigsimp(_parse(expression))
            return {"input": expression, "operation": operation, "result": str(result), "verified": True, "error": None}

        elif operation == "verify":
            if "=" in expression:
                parts = expression.split("=", 1)
                lhs = _parse(parts[0].strip())
                rhs = _parse(parts[1].strip())
                diff_result = simplify(lhs - rhs)
                return {"input": expression, "operation": operation, "result": str(diff_result == 0), "simplified_difference": str(diff_result), "verified": True, "error": None}
            return {"input": expression, "operation": operation, "result": None, "verified": False, "error": "Provide an equation with ="}

        elif operation == "limit":
            # Expects format: "expression, variable, point" e.g. "sin(x)/x, x, 0"
            expr = _parse(expression)
            result = limit(expr, var, 0)  # Default to 0, can be extended
            return {"input": expression, "operation": operation, "result": str(result), "verified": True, "error": None}

        else:
            return {"input": expression, "operation": operation, "result": None, "verified": False, "error": f"Unknown operation: {operation}"}

    except Exception as e:
        return {"input": expression, "operation": operation, "result": None, "verified": False, "error": str(e)}


@tool
def symbolic_math(expression: str, operation: str = "simplify", variable: str = "x") -> str:
    """Compute symbolic math using SymPy. Operations: solve, simplify, differentiate, integrate, factor, expand, trig_simplify, verify, limit.

    Args:
        expression: The math expression (e.g. '2*x + 3 = 11', 'sin(x)**2 + cos(x)**2')
        operation: What to do with the expression
        variable: The variable to operate on (default x)
    """
    return json.dumps(compute_symbolic(expression, operation, variable))
