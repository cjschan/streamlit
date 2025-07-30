import streamlit as st
import numpy as np
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

def plot_function_with_secant(func_str, a, h):
    """Plot the function with secant line from x=a to x=a+h."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    try:
        # Create x values for plotting
        x_range = np.linspace(-5, 5, 1000)
        
        # Evaluate function
        x = symbols('x')
        expr = sympify(func_str)
        func = lambdify(x, expr, 'numpy')
        y_range = func(x_range)
        
        # Plot the function
        ax.plot(x_range, y_range, 'b-', linewidth=2, label=f'f(x) = {func_str}')
        
        # Calculate points for secant line
        x1, x2 = a, a + h
        y1 = safe_eval_function(func_str, x1)
        y2 = safe_eval_function(func_str, x2)
        
        if y1 is not None and y2 is not None:
            # Plot points
            ax.plot([x1, x2], [y1, y2], 'ro', markersize=8, label='Points')
            
            # Calculate and plot secant line
            if h != 0:  # Avoid division by zero
                slope = (y2 - y1) / h
                # Extend secant line beyond the two points
                x_secant = np.linspace(x1 - 1, x2 + 1, 100)
                y_secant = y1 + slope * (x_secant - x1)
                ax.plot(x_secant, y_secant, 'r--', linewidth=2, 
                       label=f'Secant line (slope = {slope:.4f})')
                
                # Add slope annotation
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                ax.annotate(f'Slope = {slope:.4f}', 
                           xy=(mid_x, mid_y), xytext=(10, 10),
                           textcoords='offset points',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                           arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
            
            # Add point labels
            ax.annotate(f'({x1:.2f}, {y1:.4f})', 
                       xy=(x1, y1), xytext=(10, 10),
                       textcoords='offset points',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7))
            ax.annotate(f'({x2:.2f}, {y2:.4f})', 
                       xy=(x2, y2), xytext=(10, -20),
                       textcoords='offset points',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7))
        
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(f'Function with Secant Line from x={a} to x={a+h:.3f}')
        
        # Set fixed axis limits
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        
    except Exception as e:
        ax.text(0.5, 0.5, f'Error plotting function:\n{str(e)}', 
                transform=ax.transAxes, ha='center', va='center',
                fontsize=12, bbox=dict(boxstyle='round', facecolor='red', alpha=0.1))
        ax.set_title('Error in Function')
    
    return fig

# Streamlit App
st.title("Dynamic Secant Line Visualizer")
st.write("Visualize how secant lines change as h varies from a fixed point a.")

# Sidebar for inputs
st.sidebar.header("Parameters")

# Function selection dropdown
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
    index=0,
    help="Choose a function to visualize"
)

# Get the actual function string from the display name
func_input = [k for k, v in function_options.items() if v == selected_display][0]

# Point a input
a_value = st.sidebar.number_input(
    "Value of a (starting point):",
    value=1.0,
    step=0.1,
    format="%.2f"
)

# h slider
h_value = st.sidebar.slider(
    "Value of h:",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.01,
    format="%.3f"
)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    # Plot the function with secant line
    if func_input:
        fig = plot_function_with_secant(func_input, a_value, h_value)
        st.pyplot(fig)
    else:
        st.warning("Please enter a function to visualize.")

with col2:
    st.subheader("Current Values")
    st.write(f"**Function:** f(x) = {selected_display}")
    st.write(f"**Point a:** {a_value}")
    st.write(f"**Value h:** {h_value}")
    st.write(f"**Secant from:** x = {a_value} to x = {a_value + h_value:.3f}")
    
    # Calculate current slope if possible
    try:
        y1 = safe_eval_function(func_input, a_value)
        y2 = safe_eval_function(func_input, a_value + h_value)
        if y1 is not None and y2 is not None and h_value != 0:
            slope = (y2 - y1) / h_value
            st.write(f"**Current slope:** {slope:.6f}")
            
            # Show derivative approximation
            st.subheader("Calculus Connection")
            st.write(f"As h → 0, the secant line approaches the tangent line.")
            st.write(f"This slope approximates f'({a_value}) = {slope:.6f}")
    except:
        st.write("**Current slope:** Unable to calculate")

# Information section
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
    2. Set the point 'a' where you want to start the secant line
    3. Use the slider to adjust 'h' and watch how the secant line changes
    4. Observe how as h gets smaller, the secant line approaches the tangent line
    """)

st.write("---")
st.write("*Adjust the slider to see how secant lines approach tangent lines as h approaches 0!*")
