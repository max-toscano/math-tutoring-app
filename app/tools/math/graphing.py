"""
tools/math/graphing.py
Math visualization tool — returns Desmos graph configs.

Instead of rendering static images on the server, this tool returns
structured data that the frontend renders as an interactive Desmos graph.

The student can zoom, pan, trace points, and explore the graph.
Desmos handles asymptotes, discontinuities, and edge cases natively.

Supported graph types:
  - function_plot: one or more functions on the same axes
  - tangent_line: function with tangent line at a point
  - derivative_plot: function alongside its derivative
  - area_under_curve: shaded area between bounds
"""

import json
from sympy import symbols, diff, simplify
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)
from langchain_core.tools import tool

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)

x_sym = symbols("x")

# Colors for multiple expressions
DESMOS_COLORS = ["#6C63FF", "#FF6B6B", "#4ECDC4", "#FF9F43", "#2ECC71"]


def _parse(expr_str: str):
    """Parse expression string to SymPy."""
    cleaned = (
        expr_str
        .replace("^", "**")
        .replace("θ", "x")
        .replace("π", "pi")
        .replace("√", "sqrt")
    )
    return parse_expr(cleaned, transformations=TRANSFORMATIONS)


def _to_latex(expr_str: str) -> str:
    """Convert a Python math expression to LaTeX for Desmos."""
    try:
        from sympy import latex
        expr = _parse(expr_str)
        return latex(expr)
    except Exception:
        # Fallback: basic string replacements
        return (
            expr_str
            .replace("**", "^")
            .replace("*", " \\cdot ")
            .replace("sqrt(", "\\sqrt{")
            .replace("pi", "\\pi")
            .replace("sin(", "\\sin(")
            .replace("cos(", "\\cos(")
            .replace("tan(", "\\tan(")
            .replace("csc(", "\\csc(")
            .replace("sec(", "\\sec(")
            .replace("cot(", "\\cot(")
            .replace("log(", "\\log(")
            .replace("ln(", "\\ln(")
            .replace("exp(", "e^{")
        )


def render_graph(graph_type: str, data: dict) -> dict:
    """
    Build a Desmos graph configuration.

    Returns a structured dict that the frontend uses to render
    an interactive Desmos calculator graph.

    Returns:
        {
            "success": bool,
            "graph_type": str,
            "desmos": {
                "expressions": [...],  # Desmos expression objects
                "bounds": { "left", "right", "top", "bottom" },
            },
            "error": str | None
        }
    """
    try:
        expressions = []

        if graph_type == "function_plot":
            raw_exprs = data.get("expressions", [])
            x_range = data.get("x_range", [-10, 10])
            title = data.get("title", "")

            for i, expr_str in enumerate(raw_exprs):
                latex_expr = _to_latex(expr_str)
                expressions.append({
                    "latex": f"y = {latex_expr}",
                    "color": DESMOS_COLORS[i % len(DESMOS_COLORS)],
                })

            bounds = {
                "left": x_range[0],
                "right": x_range[1],
                "top": 10,
                "bottom": -10,
            }

        elif graph_type == "tangent_line":
            expression = data.get("expression", "x**2")
            point = data.get("point", 1)
            x_range = data.get("x_range", [-5, 5])

            # Compute tangent line
            expr = _parse(expression)
            derivative = diff(expr, x_sym)
            slope = float(derivative.subs(x_sym, point))
            y_at_point = float(expr.subs(x_sym, point))

            latex_expr = _to_latex(expression)
            tangent_latex = f"{slope:.4f}(x - {point}) + {y_at_point:.4f}"

            # Function
            expressions.append({
                "latex": f"y = {latex_expr}",
                "color": DESMOS_COLORS[0],
            })
            # Tangent line
            expressions.append({
                "latex": f"y = {tangent_latex}",
                "color": DESMOS_COLORS[1],
                "lineStyle": "DASHED",
            })
            # Point of tangency
            expressions.append({
                "latex": f"({point}, {y_at_point:.4f})",
                "color": DESMOS_COLORS[1],
                "pointStyle": "POINT",
            })

            bounds = {
                "left": x_range[0],
                "right": x_range[1],
                "top": max(10, y_at_point + 5),
                "bottom": min(-10, y_at_point - 5),
            }

        elif graph_type == "derivative_plot":
            expression = data.get("expression", "x**3")
            x_range = data.get("x_range", [-3, 3])

            expr = _parse(expression)
            derivative = simplify(diff(expr, x_sym))
            latex_expr = _to_latex(expression)
            latex_deriv = _to_latex(str(derivative))

            # f(x)
            expressions.append({
                "latex": f"y = {latex_expr}",
                "color": DESMOS_COLORS[0],
                "label": "f(x)",
            })
            # f'(x)
            expressions.append({
                "latex": f"y = {latex_deriv}",
                "color": DESMOS_COLORS[1],
                "lineStyle": "DASHED",
                "label": "f'(x)",
            })

            bounds = {
                "left": x_range[0],
                "right": x_range[1],
                "top": 10,
                "bottom": -10,
            }

        elif graph_type == "area_under_curve":
            expression = data.get("expression", "x**2")
            a = data.get("a", 0)
            b = data.get("b", 2)

            latex_expr = _to_latex(expression)

            # Function
            expressions.append({
                "latex": f"y = {latex_expr}",
                "color": DESMOS_COLORS[0],
            })
            # Shaded region (Desmos uses inequalities for shading)
            expressions.append({
                "latex": f"0 \\le y \\le {latex_expr} \\left\\{{{a} \\le x \\le {b}\\right\\}}",
                "color": DESMOS_COLORS[0],
                "fillOpacity": 0.3,
            })
            # Bounds
            expressions.append({
                "latex": f"x = {a}",
                "color": "#999999",
                "lineStyle": "DASHED",
            })
            expressions.append({
                "latex": f"x = {b}",
                "color": "#999999",
                "lineStyle": "DASHED",
            })

            bounds = {
                "left": a - 2,
                "right": b + 2,
                "top": 10,
                "bottom": -2,
            }

        else:
            return {"success": False, "graph_type": graph_type, "error": f"Unknown graph type: {graph_type}"}

        return {
            "success": True,
            "graph_type": graph_type,
            "desmos": {
                "expressions": expressions,
                "bounds": bounds,
            },
            "error": None,
        }

    except Exception as e:
        return {"success": False, "graph_type": graph_type, "error": str(e)}


@tool
def graphing(graph_type: str, data: str) -> str:
    """Generate an interactive math graph. Types: function_plot, tangent_line, derivative_plot, area_under_curve.

    Args:
        graph_type: The type of graph to render
        data: JSON string with graph parameters (e.g. '{"expressions": ["x**2", "sin(x)"], "x_range": [-5, 5]}')
    """
    d = json.loads(data) if isinstance(data, str) else data
    return json.dumps(render_graph(graph_type, d), default=str)
