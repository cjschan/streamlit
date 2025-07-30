import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sympy as sp
from sympy import symbols, lambdify, sympify
import warnings
warnings.filterwarnings('ignore')

def safe_eval_function(func_str, x_val):
    try:
        x = symbols('x')
        expr = sympify(func_str)
        func = lambdify(x, expr, 'numpy')
        return func(x_val)
    except:
        return None

def plot_function_with_secant_and_tangent(func_str, a, h, show_tangent):
    x = symbols('x')
    expr = sympify(func_str)
    func = lambdify(x, expr, 'numpy')

    # Base x-range around a
    x_vals = np.linspace(a - 5, a + 5, 1000)
    y_vals = func(x_vals)

    # Secant line (infinite extension)
    x1, x2 = a, a + h
    y1 = safe_eval_function(func_str, x1)
    y2 = safe_eval_function(func_str, x2)
    sec_slope = None
    if y1 is not None and y2 is not None and h != 0:
        sec_slope = (y2 - y1) / h
        y_sec = y1 + sec_slope * (x_vals - a)

    # Tangent line (infinite extension)
    tan_slope = None
    if show_tangent and y1 is not None:
        der = expr.diff(x)
        der_func = lambdify(x, der, 'numpy')
        tan_slope = der_func(a)
        y_tan = y1 + tan_slope * (x_vals - a)

    # Determine dynamic y-limits
    all_y = [y_vals]
    if sec_slope is not None:
        all_y.append(y_sec)
    if tan_slope is not None:
        all_y.append(y_tan)
    ys = np.concatenate(all_y)
    y_min, y_max = ys.min(), ys.max()
    y_pad = 0.05 * (y_max - y_min) if y_max > y_min else 1

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.lineplot(x=x_vals, y=y_vals, ax=ax, lw=2)

    # Plot secant line and points
    if sec_slope is not None:
        ax.plot(x_vals, y_sec, linestyle='--', linewidth=2, color='red')
        ax.scatter([x1, x2], [y1, y2], color='red', s=50)

        # Determine offsets to avoid covering important data
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        def offset(x_pt, y_pt):
            dx = 12 if x_pt < sum(xlim)/2 else -12
            dy = 12 if y_pt < sum(ylim)/2 else -12
            return dx, dy

        dx1, dy1 = offset(x1, y1)
        dx2, dy2 = offset(x2, y2)

        ax.annotate(
            f'({x1:.2f}, {y1:.4f})',
            xy=(x1, y1),
            xytext=(dx1, dy1),
            textcoords='offset points',
            fontsize=14,
            fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'),
            arrowprops=None
        )
        ax.annotate(
            f'({x2:.2f}, {y2:.4f})',
            xy=(x2, y2),
            xytext=(dx2, dy2),
            textcoords='offset points',
            fontsize=14,
            fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'),
            arrowprops=None
        )

    # Plot tangent line if requested
    if tan_slope is not None:
        ax.plot(x_vals, y_tan, linewidth=2, color='green')

    # Center axes
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    ax.set_xlim(x_vals.min(), x_vals.max())
    ax.set_ylim(y_min - y_pad, y_max + y_pad)
    ax.grid(True, linestyle=':', color='lightgray')

    return fig

st.title("Dynamic Secant and Tangent Line Visualizer")

st.sidebar.header("Parameters")
function_options = {
    "x**2": "x²",
    "x**3": "x³",
    "sin(x)": "sin(x)",
    "cos(x)": "cos(x)",
    "exp(x)": "eˣ",
    "log(x)": "ln(x)",
    "sqrt(x)": "√x",
    "1/x": "1/x",
    "x**3 - 2*x": "x³ - 2x",
    "x**2 - 4": "x² - 4",
    "2*x + 1": "2x + 1",
    "x**4 - x**2": "x⁴ - x²"
}

selected = st.sidebar.selectbox(
    "Select function f(x):",
    options=list(function_options.values()),
    index=0
)
func_input = [k for k, v in function_options.items() if v == selected][0]

a_val = st.sidebar.number_input(
    "Value of a:",
    value=1.0,
    step=0.1,
    format="%.2f"
)
h_val = st.sidebar.slider(
    "Value of h:",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.01,
    format="%.3f"
)
show_tan = st.sidebar.checkbox("Show tangent line at x = a", value=False)

col1, col2 = st.columns([2, 1])

with col1:
    fig = plot_function_with_secant_and_tangent(func_input, a_val, h_val, show_tan)
    st.pyplot(fig)

with col2:
    st.subheader("Current Values")
    st.write(f"Function: f(x) = {selected}")
    st.write(f"Point a: {a_val}")
    st.write(f"Value h: {h_val}")
    y1 = safe_eval_function(func_input, a_val)
    y2 = safe_eval_function(func_input, a_val + h_val)
    if y1 is not None and y2 is not None and h_val != 0:
        sec = (y2 - y1) / h_val
        st.write(f"Secant slope: {sec:.6f}")
    if show_tan and y1 is not None:
        der = sympify(func_input).diff(symbols('x'))
        der_func = lambdify(symbols('x'), der, 'numpy')
        ts = der_func(a_val)
        st.write(f"Tangent slope: {ts:.6f}")
