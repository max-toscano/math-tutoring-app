"""
graph_engine.py
Server-side graph generation using matplotlib.

The AI sends a structured graph request, this engine renders it to a PNG
and returns base64-encoded image data. Supports multiple graph types
covering all Calculus 1 visual needs.
"""

import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Any

# ─── Theme (matches app Colors) ───────────────────────────────────────────────

COLORS = {
    'primary': '#6C63FF',
    'secondary': '#FF6B6B',
    'teal': '#4ECDC4',
    'orange': '#FF9F43',
    'green': '#2ECC71',
    'text': '#1A1A2E',
    'muted': '#9CA3AF',
    'bg': '#FAFAFA',
}

PALETTE = [COLORS['primary'], COLORS['secondary'], COLORS['teal'],
           COLORS['orange'], COLORS['green'], '#9B59B6', '#E74C3C']

plt.rcParams.update({
    'figure.facecolor': COLORS['bg'],
    'axes.facecolor': COLORS['bg'],
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.grid': True,
    'grid.alpha': 0.25,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.labelcolor': COLORS['text'],
    'xtick.color': COLORS['text'],
    'ytick.color': COLORS['text'],
})


# ─── Safe Math Evaluator ──────────────────────────────────────────────────────

SAFE_MATH_NAMES = {
    'x': None, 't': None,  # placeholders, replaced at eval time
    'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
    'arcsin': np.arcsin, 'arccos': np.arccos, 'arctan': np.arctan,
    'sqrt': np.sqrt, 'abs': np.abs, 'log': np.log, 'ln': np.log,
    'log10': np.log10, 'log2': np.log2,
    'exp': np.exp, 'e': np.e, 'pi': np.pi,
    'inf': np.inf,
}


def safe_eval(expr: str, x: np.ndarray) -> np.ndarray:
    """Evaluate a math expression string safely over an array of x values."""
    namespace = {**SAFE_MATH_NAMES, 'x': x, 't': x, 'np': np}
    # Replace ^ with ** for Python
    expr = expr.replace('^', '**')
    try:
        result = eval(expr, {"__builtins__": {}}, namespace)
        if isinstance(result, (int, float)):
            return np.full_like(x, result, dtype=float)
        return np.array(result, dtype=float)
    except Exception as e:
        raise ValueError(f"Cannot evaluate expression '{expr}': {e}")


# ─── Figure → Base64 ──────────────────────────────────────────────────────────

def fig_to_base64(fig: plt.Figure, dpi: int = 150) -> str:
    """Render a matplotlib figure to a base64-encoded PNG string."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


# ─── Graph Type Renderers ─────────────────────────────────────────────────────

def render_function_plot(data: dict) -> str:
    """Plot one or more functions.
    data: { functions: [{expr, label?, color?, style?}], domain: [a,b], title?, xlabel?, ylabel?, ylim? }
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    domain = data.get('domain', [-5, 5])
    x = np.linspace(domain[0], domain[1], 500)

    for i, fn in enumerate(data.get('functions', [])):
        y = safe_eval(fn['expr'], x)
        color = fn.get('color', PALETTE[i % len(PALETTE)])
        style = fn.get('style', '-')
        label = fn.get('label', fn['expr'])
        ax.plot(x, y, color=color, linewidth=2.5, linestyle=style, label=label)

    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    if data.get('ylim'):
        ax.set_ylim(data['ylim'])
    ax.set_xlabel(data.get('xlabel', 'x'))
    ax.set_ylabel(data.get('ylabel', 'y'))
    ax.set_title(data.get('title', ''), fontweight='bold', fontsize=14)
    if len(data.get('functions', [])) > 1:
        ax.legend(framealpha=0.9, fontsize=10)
    plt.tight_layout()
    return fig_to_base64(fig)


def render_tangent_line(data: dict) -> str:
    """Plot a function with tangent line at a point.
    data: { function: expr, point: x_val, domain: [a,b], title? }
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    domain = data.get('domain', [-2, 6])
    x = np.linspace(domain[0], domain[1], 500)
    a = data['point']

    y = safe_eval(data['function'], x)
    ax.plot(x, y, color=COLORS['primary'], linewidth=2.5, label=f"f(x) = {data['function']}")

    # Compute derivative numerically
    h = 1e-7
    x_a = np.array([a])
    fa = safe_eval(data['function'], x_a)[0]
    fa_h = safe_eval(data['function'], np.array([a + h]))[0]
    slope = (fa_h - fa) / h

    # Tangent line
    tang_x = np.linspace(a - 1.5, a + 1.5, 50)
    tang_y = fa + slope * (tang_x - a)
    ax.plot(tang_x, tang_y, color=COLORS['secondary'], linewidth=2, linestyle='--',
            label=f'Tangent (slope = {slope:.2f})')
    ax.plot(a, fa, 'o', color=COLORS['secondary'], markersize=9, zorder=5)

    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_title(data.get('title', f'Tangent Line at x = {a}'), fontweight='bold', fontsize=14)
    ax.legend(framealpha=0.9, fontsize=10)
    plt.tight_layout()
    return fig_to_base64(fig)


def render_riemann_sum(data: dict) -> str:
    """Plot Riemann sum approximation.
    data: { function: expr, interval: [a,b], n: int, method: 'left'|'right'|'midpoint', title? }
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    a, b = data['interval']
    n = data.get('n', 8)
    method = data.get('method', 'left')
    x = np.linspace(a, b, 500)
    y = safe_eval(data['function'], x)
    ax.plot(x, y, color=COLORS['primary'], linewidth=2.5, zorder=3)

    dx = (b - a) / n
    total_area = 0
    for i in range(n):
        if method == 'left':
            xi = a + i * dx
        elif method == 'right':
            xi = a + (i + 1) * dx
        else:  # midpoint
            xi = a + (i + 0.5) * dx
        height = safe_eval(data['function'], np.array([xi]))[0]
        total_area += height * dx
        rect = patches.Rectangle(
            (a + i * dx, 0), dx, height,
            facecolor=COLORS['primary'] + '30', edgecolor=COLORS['primary'], linewidth=1, zorder=2)
        ax.add_patch(rect)

    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_title(data.get('title', f'{method.title()} Sum (n={n}), Area ≈ {total_area:.4f}'),
                 fontweight='bold', fontsize=13)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.tight_layout()
    return fig_to_base64(fig)


def render_area_between(data: dict) -> str:
    """Shade area between two curves.
    data: { top: expr, bottom: expr, interval: [a,b], title? }
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    a, b = data['interval']
    x = np.linspace(a - 0.5, b + 0.5, 500)
    x_fill = np.linspace(a, b, 500)

    y_top = safe_eval(data['top'], x)
    y_bot = safe_eval(data['bottom'], x)
    y_top_fill = safe_eval(data['top'], x_fill)
    y_bot_fill = safe_eval(data['bottom'], x_fill)

    ax.plot(x, y_top, color=COLORS['primary'], linewidth=2.5, label=f"f(x) = {data['top']}")
    ax.plot(x, y_bot, color=COLORS['secondary'], linewidth=2.5, label=f"g(x) = {data['bottom']}")
    ax.fill_between(x_fill, y_bot_fill, y_top_fill, alpha=0.25, color=COLORS['teal'], label='Area')
    ax.plot([a, b], [safe_eval(data['top'], np.array([a]))[0], safe_eval(data['top'], np.array([b]))[0]],
            'o', color='black', markersize=7, zorder=5)

    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_title(data.get('title', 'Area Between Curves'), fontweight='bold', fontsize=14)
    ax.legend(framealpha=0.9, fontsize=9)
    plt.tight_layout()
    return fig_to_base64(fig)


def render_derivative_analysis(data: dict) -> str:
    """Triple panel: f, f', f'' with colored regions.
    data: { function: expr, derivative: expr, second_derivative: expr, domain: [a,b], title? }
    """
    fig, axes = plt.subplots(3, 1, figsize=(7, 8), sharex=True)
    domain = data.get('domain', [-3, 5])
    x = np.linspace(domain[0], domain[1], 500)

    # f(x)
    y = safe_eval(data['function'], x)
    axes[0].plot(x, y, color=COLORS['primary'], linewidth=2.5)
    axes[0].set_ylabel('f(x)', fontweight='bold')
    axes[0].set_title(data.get('title', 'Derivative Analysis'), fontweight='bold', fontsize=14)

    # f'(x)
    if data.get('derivative'):
        yp = safe_eval(data['derivative'], x)
    else:
        yp = np.gradient(y, x)
    axes[1].plot(x, yp, color=COLORS['green'], linewidth=2.5)
    axes[1].fill_between(x, yp, 0, where=(yp > 0), alpha=0.15, color=COLORS['green'], label='increasing')
    axes[1].fill_between(x, yp, 0, where=(yp < 0), alpha=0.15, color=COLORS['secondary'], label='decreasing')
    axes[1].axhline(0, color='black', linewidth=0.8)
    axes[1].set_ylabel("f'(x)", fontweight='bold')
    axes[1].legend(fontsize=9)

    # f''(x)
    if data.get('second_derivative'):
        ypp = safe_eval(data['second_derivative'], x)
    else:
        ypp = np.gradient(yp, x)
    axes[2].plot(x, ypp, color=COLORS['orange'], linewidth=2.5)
    axes[2].fill_between(x, ypp, 0, where=(ypp > 0), alpha=0.15, color=COLORS['teal'], label='concave up')
    axes[2].fill_between(x, ypp, 0, where=(ypp < 0), alpha=0.15, color=COLORS['orange'], label='concave down')
    axes[2].axhline(0, color='black', linewidth=0.8)
    axes[2].set_ylabel("f''(x)", fontweight='bold')
    axes[2].set_xlabel('x')
    axes[2].legend(fontsize=9)

    plt.tight_layout()
    return fig_to_base64(fig)


def render_limit(data: dict) -> str:
    """Visualize a limit with approach arrows and open/closed circles.
    data: { function: expr, approach: x_val, limit_value: y_val, domain: [a,b], title? }
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    domain = data.get('domain', [-5, 5])
    x = np.linspace(domain[0], domain[1], 1000)
    c = data['approach']
    L = data['limit_value']

    # Avoid the exact point to show the hole
    mask = np.abs(x - c) > 0.02
    y = safe_eval(data['function'], x)
    ax.plot(x[mask], y[mask], color=COLORS['primary'], linewidth=2.5)

    # Open circle at the limit point
    ax.plot(c, L, 'o', color=COLORS['secondary'], markersize=10, zorder=5,
            markerfacecolor='white', markeredgewidth=2.5)

    # Dashed line at limit value
    ax.axhline(L, color=COLORS['secondary'], linewidth=1.5, linestyle='--', alpha=0.5)

    ax.annotate(f'lim = {L}', xy=(c, L), xytext=(c + 1.5, L + 0.5),
                fontsize=13, fontweight='bold', color=COLORS['secondary'],
                arrowprops=dict(arrowstyle='->', color=COLORS['secondary'], lw=2),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=COLORS['secondary'], alpha=0.9))

    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_title(data.get('title', f'Limit as x → {c}'), fontweight='bold', fontsize=14)
    ax.set_xlabel('x')
    plt.tight_layout()
    return fig_to_base64(fig)


def render_volume_revolution(data: dict) -> str:
    """3D surface of revolution.
    data: { function: expr, interval: [a,b], axis: 'x'|'y', title? }
    """
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111, projection='3d')
    a, b = data['interval']

    u = np.linspace(a, b, 100)
    v = np.linspace(0, 2 * np.pi, 60)
    U, V = np.meshgrid(u, v)
    R = safe_eval(data['function'], U)
    Y = R * np.cos(V)
    Z = R * np.sin(V)

    ax.plot_surface(U, Y, Z, alpha=0.45, cmap='cool', edgecolor='none')

    # Original curve
    t = np.linspace(a, b, 100)
    ax.plot(t, safe_eval(data['function'], t), np.zeros_like(t),
            color=COLORS['secondary'], linewidth=3)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title(data.get('title', 'Volume of Revolution'), fontweight='bold', fontsize=13)
    ax.view_init(elev=20, azim=-60)
    plt.tight_layout()
    return fig_to_base64(fig)


def render_newtons_method(data: dict) -> str:
    """Newton's method iterations.
    data: { function: expr, derivative: expr, x0: float, iterations: int, domain: [a,b], title? }
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    domain = data.get('domain', [-1, 5])
    x = np.linspace(domain[0], domain[1], 500)
    y = safe_eval(data['function'], x)
    ax.plot(x, y, color=COLORS['primary'], linewidth=2.5)
    ax.axhline(0, color='black', linewidth=0.5)

    xn = data['x0']
    for i in range(data.get('iterations', 4)):
        fn = safe_eval(data['function'], np.array([xn]))[0]
        fpn = safe_eval(data['derivative'], np.array([xn]))[0]
        if abs(fpn) < 1e-12:
            break
        xn_new = xn - fn / fpn
        ax.plot(xn, fn, 'o', color=COLORS['secondary'], markersize=7, zorder=5)
        ax.plot([xn, xn_new], [fn, 0], '--', color=COLORS['orange'], linewidth=1.5)
        ax.plot(xn_new, 0, 's', color=COLORS['green'], markersize=6, zorder=5)
        # Label iteration
        ax.annotate(f'x{i+1}', xy=(xn_new, 0), xytext=(xn_new, -0.5),
                    fontsize=9, fontweight='bold', ha='center', color=COLORS['green'])
        xn = xn_new

    ax.set_title(data.get('title', "Newton's Method"), fontweight='bold', fontsize=14)
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    plt.tight_layout()
    return fig_to_base64(fig)


# ─── Router ────────────────────────────────────────────────────────────────────

GRAPH_RENDERERS = {
    'function_plot': render_function_plot,
    'tangent_line': render_tangent_line,
    'riemann_sum': render_riemann_sum,
    'area_between': render_area_between,
    'derivative_analysis': render_derivative_analysis,
    'limit': render_limit,
    'volume_revolution': render_volume_revolution,
    'newtons_method': render_newtons_method,
}


def generate_graph(graph_type: str, data: dict) -> str:
    """Generate a graph and return base64-encoded PNG.

    Args:
        graph_type: one of GRAPH_RENDERERS keys
        data: type-specific parameters

    Returns:
        Base64-encoded PNG string
    """
    renderer = GRAPH_RENDERERS.get(graph_type)
    if not renderer:
        raise ValueError(f"Unknown graph type '{graph_type}'. Valid: {list(GRAPH_RENDERERS.keys())}")
    return renderer(data)
