import streamlit as st
import pandas as pd
import numpy as np
import datetime

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



col1, col2, col3, col4, col5 = st.columns([2,1,1.5,1,1])

with col1:
    question = "BlueButton Marketing, Inc. worked in the office for the month of September. The amount of electricity the company used equaled $12,000 for the month. On October 1, the business received the bill and wrote a check to the electric company on October 2."
    st.write(question)

with col2:
    date_1 = st.date_input("Date", key="7", format="MM/DD/YYYY",label_visibility="visible")
    date_2 = st.date_input("Date", key="8", format="MM/DD/YYYY",label_visibility="collapsed")

with col3:
    account_1 = st.selectbox(
        'Account',
        ('Electricity bill','Accrued expenses'),key="1"
        )
    account_2 = st.selectbox(
        'Account_1',
        ('Electricity bill','Accrued expenses'),key="2",label_visibility="collapsed"
        )
with col4:
    debit_1 = st.text_input('Debit',key="3")
    debit_2 = st.text_input('Debit1',key="4",label_visibility="collapsed")

with col5:
    credit_1 = st.text_input('Credit',key="5")
    credit_2 = st.text_input('Credit1',key="6",label_visibility="collapsed")

st.write("Notes: Auto-complete account names and randomization to be added")
