"""
tools/math/numerical_math.py
Numerical math computation using NumPy + SymPy.

Handles: numerical evaluation, root finding, numerical integration,
Riemann sums, Newton's method, function evaluation at points,
numerical derivatives, statistical calculations.

This is a real tool — NumPy computes floating-point results
that LLMs cannot produce accurately.
"""

import numpy as np
from sympy import symbols, lambdify, sympify
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

x = symbols("x")


def _parse(expr_str: str):
    """Parse expression string to SymPy."""
    cleaned = expr_str.replace("^", "**").replace("θ", "theta").replace("π", "pi").replace("√", "sqrt")
    return parse_expr(cleaned, transformations=TRANSFORMATIONS)


def _to_numpy_func(expr_str: str):
    """Convert a string expression to a callable NumPy function."""
    expr = _parse(expr_str)
    return lambdify(x, expr, modules=["numpy"])


def compute_numerical(expression: str, operation: str, params: dict = None) -> dict:
    """
    Perform a numerical computation.

    Args:
        expression: Math expression as string.
        operation: evaluate | roots | numerical_integral | riemann_sum |
                   newtons_method | function_table | numerical_derivative
        params: Operation-specific parameters.

    Returns:
        Dict with input, operation, result, error.
    """
    params = params or {}

    try:
        if operation == "evaluate":
            # Evaluate f(x) at a specific point
            point = params.get("at", 0)
            f = _to_numpy_func(expression)
            result = float(f(point))
            return {"input": expression, "operation": operation, "at": point, "result": result, "error": None}

        elif operation == "function_table":
            # Evaluate f(x) at multiple points
            start = params.get("start", -5)
            end = params.get("end", 5)
            steps = params.get("steps", 11)
            f = _to_numpy_func(expression)
            x_vals = np.linspace(start, end, steps)
            y_vals = f(x_vals)
            table = [{"x": round(float(xv), 4), "y": round(float(yv), 4)} for xv, yv in zip(x_vals, y_vals)]
            return {"input": expression, "operation": operation, "table": table, "error": None}

        elif operation == "numerical_integral":
            # Trapezoidal numerical integration
            a = params.get("a", 0)
            b = params.get("b", 1)
            n_points = params.get("n", 1000)
            f = _to_numpy_func(expression)
            x_vals = np.linspace(a, b, n_points)
            y_vals = f(x_vals)
            # np.trapezoid in newer numpy, np.trapz in older
            trapz_fn = getattr(np, "trapezoid", None) or np.trapz
            result = float(trapz_fn(y_vals, x_vals))
            return {"input": expression, "operation": operation, "a": a, "b": b, "result": round(result, 8), "error": None}

        elif operation == "riemann_sum":
            # Left, right, or midpoint Riemann sum
            a = params.get("a", 0)
            b = params.get("b", 1)
            n = params.get("n", 6)
            method = params.get("method", "left")
            f = _to_numpy_func(expression)
            dx = (b - a) / n

            if method == "left":
                sample_points = np.array([a + i * dx for i in range(n)])
            elif method == "right":
                sample_points = np.array([a + (i + 1) * dx for i in range(n)])
            elif method == "midpoint":
                sample_points = np.array([a + (i + 0.5) * dx for i in range(n)])
            else:
                return {"error": f"Unknown method: {method}"}

            heights = f(sample_points)
            rectangles = [{"x": round(float(sp), 4), "height": round(float(h), 4), "area": round(float(h * dx), 4)} for sp, h in zip(sample_points, heights)]
            total = float(np.sum(heights * dx))

            return {"input": expression, "operation": operation, "method": method, "n": n, "a": a, "b": b, "dx": round(dx, 4), "rectangles": rectangles, "total_area": round(total, 6), "error": None}

        elif operation == "newtons_method":
            # Newton's method for root finding
            x0 = params.get("x0", 1.0)
            max_iter = params.get("max_iter", 20)
            tol = params.get("tol", 1e-10)

            expr = _parse(expression)
            from sympy import diff as sym_diff
            expr_prime = sym_diff(expr, symbols("x"))
            f = lambdify(symbols("x"), expr, modules=["numpy"])
            fp = lambdify(symbols("x"), expr_prime, modules=["numpy"])

            iterations = []
            xn = x0
            for i in range(max_iter):
                fxn = float(f(xn))
                fpxn = float(fp(xn))
                if abs(fpxn) < 1e-15:
                    return {"error": "Derivative near zero — method diverges"}
                xn1 = xn - fxn / fpxn
                iterations.append({"iteration": i + 1, "x": round(float(xn), 10), "f(x)": round(fxn, 10)})
                if abs(xn1 - xn) < tol:
                    iterations.append({"iteration": i + 2, "x": round(float(xn1), 10), "f(x)": round(float(f(xn1)), 10)})
                    return {"input": expression, "operation": operation, "root": round(float(xn1), 10), "iterations": iterations, "converged": True, "error": None}
                xn = xn1

            return {"input": expression, "operation": operation, "root": round(float(xn), 10), "iterations": iterations, "converged": False, "error": "Did not converge"}

        elif operation == "numerical_derivative":
            # Numerical derivative at a point using central difference
            point = params.get("at", 0)
            h = params.get("h", 1e-8)
            f = _to_numpy_func(expression)
            result = float((f(point + h) - f(point - h)) / (2 * h))
            return {"input": expression, "operation": operation, "at": point, "result": round(result, 8), "error": None}

        else:
            return {"input": expression, "operation": operation, "result": None, "error": f"Unknown operation: {operation}"}

    except Exception as e:
        return {"input": expression, "operation": operation, "result": None, "error": str(e)}


@tool
def numerical_math(expression: str, operation: str, params: str = "{}") -> str:
    """Compute numerical math using NumPy. Operations: evaluate, function_table, numerical_integral, riemann_sum, newtons_method, numerical_derivative.

    Args:
        expression: The math expression (e.g. 'x**2 * sin(x)')
        operation: What to compute
        params: JSON string of operation parameters (e.g. '{"a": 0, "b": 1, "n": 100}')
    """
    p = json.loads(params) if isinstance(params, str) else params
    return json.dumps(compute_numerical(expression, operation, p))
