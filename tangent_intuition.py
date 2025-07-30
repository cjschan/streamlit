import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sympy as sp
from sympy import symbols, lambdify, sympify
import warnings
warnings.filterwarnings('ignore')

def safe_eval_function(func_str, x_val):
    """Safely evaluate a mathematical function at a given x value."""
    try:
        x = symbols('x')
        expr = sympify(func_str)
        func = lambdify(x, expr, 'numpy')
        return func(x_val)
    except:
        return None

def plot_function_with_secant_and_tangent(func_str, a, h, show_tangent):
    """Plot the function with secant line from x=a to x=a+h and optional tangent at x=a using seaborn."""
    # Prepare symbolic and numeric functions
    x = symbols('x')
    expr = sympify(func_str)
    func = lambdify(x, expr, 'numpy')
    x_range = np.linspace(-5, 5, 1000)
    y_range = func(x_range)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.lineplot(x=x_range, y=y_range, ax=ax, label=f'f(x) = {func_str}', lw=2.5)

    # Secant line
    x1, x2 = a, a + h
    y1 = safe_eval_function(func_str, x1)
    y2 = safe_eval_function(func_str, x2)
    if y1 is not None and y2 is not None and h != 0:
        secant_slope = (y2 - y1) / h
        # Plot secant points
        ax.scatter([x1, x2], [y1, y2], color='red', s=50, label='Secant points')
        # Plot secant line
        x_sec = np.linspace(-5, 5, 100)
        y_sec = y1 + secant_slope * (x_sec - x1)
        ax.plot(x_sec, y_sec, linestyle='--', linewidth=2, color='red',
                label=f'Secant (slope={secant_slope:.4f})')

    # Tangent line
    if show_tangent and y1 is not None:
        derivative_expr = expr.diff(x)
        derivative_func = lambdify(x, derivative_expr, 'numpy')
        tangent_slope = derivative_func(a)
        x_tan = np.linspace(-5, 5, 100)
        y_tan = y1 + tangent_slope * (x_tan - a)
        ax.plot(x_tan, y_tan, linewidth=2, color='green',
                label=f'Tangent (slope={tangent_slope:.4f})')

    # Annotation for point a
    if y1 is not None:
        ax.annotate(f'({a:.2f}, {y1:.4f})',
                    xy=(a, y1),
                    xytext=(a + 0.5, y1 + 0.5),
                    arrowprops=dict(arrowstyle='->', lw=1))

    # Axis styling
    ax.set_title(f'Function with Secant and Tangent at x = {a}')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.grid(True, linestyle=':', color='lightgray')
    ax.legend()

    return fig

# Streamlit App
st.title("Dynamic Secant and Tangent Line Visualizer")
st.write("Visualize how secant and tangent lines change for a fixed point a and varying h.")

# Sidebar inputs
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

selected_display = st.sidebar.selectbox(
    "Select function f(x):",
    options=list(function_options.values()),
    index=0
)
func_input = [k for k, v in function_options.items() if v == selected_display][0]

a_value = st.sidebar.number_input(
    "Value of a (starting point):",
    value=1.0,
    step=0.1,
    format="%.2f"
)

h_value = st.sidebar.slider(
    "Value of h:",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.01,
    format="%.3f"
)

show_tangent = st.sidebar.checkbox(
    "Show tangent line at x = a",
    value=False
)

# Main display
col1, col2 = st.columns([2, 1])

with col1:
    fig = plot_function_with_secant_and_tangent(func_input, a_value, h_value, show_tangent)
    st.pyplot(fig)

with col2:
    st.subheader("Current Values")
    st.write(f"**Function:** f(x) = {selected_display}")
    st.write(f"**Point a:** {a_value}")
    st.write(f"**Value h:** {h_value}")
    st.write(f"**Secant from:** x = {a_value} to x = {a_value + h_value:.3f}")
    y1 = safe_eval_function(func_input, a_value)
    y2 = safe_eval_function(func_input, a_value + h_value)
    if y1 is not None and y2 is not None and h_value != 0:
        sec_slope = (y2 - y1) / h_value
        st.write(f"**Secant slope:** {sec_slope:.6f}")
    if show_tangent and y1 is not None:
        derivative_expr = sympify(func_input).diff(symbols('x'))
        derivative_func = lambdify(symbols('x'), derivative_expr, 'numpy')
        tan_slope = derivative_func(a_value)
        st.write(f"**Tangent slope:** {tan_slope:.6f}")

with st.expander("Available functions"):
    st.write("""
    The dropdown includes these pre-selected functions:

    **Polynomial Functions:**
    - x² (quadratic)
    - x³ (cubic)
    - x³ - 2x (cubic with linear term)
    - x² - 4 (shifted parabola)
    - x⁴ - x² (quartic)
    - 2x + 1 (linear)

    **Transcendental Functions:**
    - sin(x) (sine wave)
    - cos(x) (cosine wave)
    - eˣ (exponential)
    - ln(x) (natural logarithm)
    - √x (square root)
    - 1/x (reciprocal/hyperbola)

    **Instructions:**
    1. Select a function from the dropdown
    2. Set the point a where the secant and tangent originate
    3. Adjust h to observe the secant line between x = a and x = a + h
    4. Check the box to display the tangent line at x = a
    """)

st.write("---")
st.write("Adjust parameters to explore how the secant and tangent lines relate to the function.")
