import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

hide = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        body {overflow: hidden;}
        div.block-container {padding-top:1rem;}
        div.block-container {padding-bottom:1rem;}
        thead tr th:first-child {display:none}
        tbody th {display:none}
        </style>
        """

st.markdown(hide, unsafe_allow_html=True)

question = "BlueButton Marketing, Inc. worked in the office for the month of September. The amount of electricity the company used equaled $12,000 for the month. On October 1, the business received the bill and wrote a check to the electric company on October 2."



col1, col2, col3 = st.columns([1.5,1.5,1.5])

with col1:
    st.write(question)

with col2:
    title = st.text_input('Account', '')
