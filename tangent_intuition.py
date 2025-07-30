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

    trig = func_str in ("sin(x)", "cos(x)")

    if trig:
        x_vals = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
        y_min_plot, y_max_plot = -1, 1
        x_min_plot, x_max_plot = -2 * np.pi, 2 * np.pi
    else:
        x_vals = np.linspace(-3, 3, 1000)
        y_min_plot, y_max_plot = -3, 3
        x_min_plot, x_max_plot = -3, 3

    y_vals = func(x_vals)

    x1, x2 = a, a + h
    y1 = safe_eval_function(func_str, x1)
    y2 = safe_eval_function(func_str, x2)

    sec_slope = None
    if y1 is not None and y2 is not None and h != 0:
        sec_slope = (y2 - y1) / h
        x_sec = np.linspace(x1, x2, 100)
        y_sec = y1 + sec_slope * (x_sec - x1)

    tan_slope = None
    if show_tangent and y1 is not None:
        der = expr.diff(x)
        der_func = lambdify(x, der, 'numpy')
        tan_slope = der_func(a)
        x_tan = np.linspace(x_min_plot, x_max_plot, 100)
        y_tan = y1 + tan_slope * (x_tan - a)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.lineplot(x=x_vals, y=y_vals, ax=ax, label=f'f(x) = {func_str}', lw=2)

    if sec_slope is not None:
        ax.scatter([x1, x2], [y1, y2], color='red', s=50, label='Secant points')
        ax.plot(x_sec, y_sec, linestyle='--', linewidth=2, color='red',
                label=f'Secant (slope={sec_slope:.4f})')

    if tan_slope is not None:
        ax.plot(x_tan, y_tan, linewidth=2, color='green',
                label=f'Tangent (slope={tan_slope:.4f})')

    if y1 is not None:
        ax.annotate(f'({a:.2f}, {y1:.4f})',
                    xy=(a, y1),
                    xytext=(a + 0.2, y1 + 0.2),
                    arrowprops=dict(arrowstyle='->', lw=1))

    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    ax.set_xlim(x_min_plot, x_max_plot)
    ax.set_ylim(y_min_plot, y_max_plot)
    ax.grid(True, linestyle=':', color='lightgray')
    ax.legend()

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