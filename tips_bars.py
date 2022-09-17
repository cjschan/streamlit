import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

hide = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        body {overflow: hidden;}
        div.block-container {padding-top:1rem;}
        div.block-container {padding-bottom:1rem;}
        </style>
        """

st.markdown(hide, unsafe_allow_html=True)

tips = sns.load_dataset('tips')
tips.columns = ["Total bill", "Tip", "Sex", "Smoker", "Day", "Time", "Party size"]

# st.header("Visualizing the tips dataset")

col1, col2 = st.columns([1,3])

with col1:

    categorical = st.selectbox(
        "Categorical variable",
        [
            "Day",
            "Party size",
            "Time",
            "Sex",
            "Smoker"
        ]
    )

    if categorical="Day"
            group = st.selectbox(
                "Grouping",
                [None, "Party size","Time","Sex","Smoker"]
            )

    elif categorical="Party size"
            group = st.selectbox(
                "Grouping",
                [None, "Day","Time","Sex","Smoker"]
            )

    elif categorical="Time"
            group = st.selectbox(
                "Grouping",
                [None, "Day","Party size","Sex","Smoker"]
            )

    elif categorical="Sex"
            group = st.selectbox(
                "Grouping",
                [None, "Day","Party size","Smoker","Time"]
            )

    else:
            group = st.selectbox(
                "Grouping",
                [None, "Day","Party size","Sex","Time"]
            )

with col2:
    fig, ax = plt.subplots()

    sns.countplot(x=categorical, hue=group, data=tips)

    ax.set_xlabel(categorical, fontsize=14)
    ax.set_ylabel("Count", fontsize=14)

    st.pyplot(fig)
