import streamlit as st
import numpy as np
import plotly.graph_objects as go
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
    """Plot the function with secant line from x=a to x=a+h using Plotly."""
    
    try:
        # Create x values for plotting
        x_range = np.linspace(-5, 5, 1000)
        
        # Evaluate function
        x = symbols('x')
        expr = sympify(func_str)
        func = lambdify(x, expr, 'numpy')
        y_range = func(x_range)
        
        # Create plotly figure
        fig = go.Figure()
        
        # Plot the function
        fig.add_trace(go.Scatter(
            x=x_range, 
            y=y_range, 
            mode='lines', 
            name=f'f(x) = {func_str}', 
            line=dict(color='blue', width=3)
        ))
        
        # Calculate points for secant line
        x1, x2 = a, a + h
        y1 = safe_eval_function(func_str, x1)
        y2 = safe_eval_function(func_str, x2)
        
        if y1 is not None and y2 is not None:
            # Plot points
            fig.add_trace(go.Scatter(
                x=[x1, x2], 
                y=[y1, y2], 
                mode='markers', 
                name='Points', 
                marker=dict(color='red', size=10)
            ))
            
            # Calculate and plot secant line
            if h != 0:  # Avoid division by zero
                slope = (y2 - y1) / h
                # Extend secant line beyond the two points
                x_secant = np.linspace(-5, 5, 100)
                y_secant = y1 + slope * (x_secant - x1)
                fig.add_trace(go.Scatter(
                    x=x_secant, 
                    y=y_secant, 
                    mode='lines', 
                    name=f'Secant line (slope = {slope:.4f})',
                    line=dict(color='red', width=2, dash='dash')
                ))
                
                # Add annotations for points
                fig.add_annotation(
                    x=x1, y=y1,
                    text=f'({x1:.2f}, {y1:.4f})',
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor='blue',
                    bgcolor='lightblue',
                    bordercolor='blue'
                )
                
                fig.add_annotation(
                    x=x2, y=y2,
                    text=f'({x2:.2f}, {y2:.4f})',
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor='blue',
                    bgcolor='lightblue',
                    bordercolor='blue'
                )
        
        # Configure layout with solid axes
        fig.update_layout(
            title=f'Function with Secant Line from x={a} to x={a+h:.3f}',
            xaxis=dict(
                title='x',
                range=[-5, 5],
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='black',
                showline=True,
                linewidth=2,
                linecolor='black'
            ),
            yaxis=dict(
                title='y',
                range=[-5, 5],
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='black',
                showline=True,
                linewidth=2,
                linecolor='black'
            ),
            showlegend=True,
            width=800,
            height=600,
            plot_bgcolor='white'
        )
        
        return fig
        
    except Exception as e:
        # Create error figure
        fig = go.Figure()
        fig.add_annotation(
            text=f'Error plotting function: {str(e)}', 
            xref="paper", yref="paper", 
            x=0.5, y=0.5, 
            showarrow=False,
            font=dict(size=16, color='red')
        )
        fig.update_layout(
            title='Error in Function',
            xaxis=dict(title='x', range=[-5, 5]),
            yaxis=dict(title='y', range=[-5, 5])
        )
        return fig

# Streamlit App
st.title("Visualizing Secant Lines and Tangent Lines")
st.write("Visualize how secant lines change as h varies from a fixed point a.")

# Sidebar for inputs
st.sidebar.header("Parameters")

# Function selection dropdown
function_options = {
    "x**2": r"$x^2$",
    "x**3": r"$x^3$",
    "sin(x)": r"$\sin(x)$",
    "cos(x)": r"$\cos(x)$",
    "exp(x)": r"$e^x$",
    "log(x)": r"$\ln(x)$",
    "sqrt(x)": r"$\sqrt{x}$",
    "1/x": r"$\frac{1}{x}$",
    "x**3 - 2*x": r"$x^3 - 2x$",
    "x**2 - 4": r"$x^2 - 4$",
    "2*x + 1": r"$2x + 1$",
    "x**4 - x**2": r"$x^4 - x^2$"
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
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select a function to visualize.")

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
