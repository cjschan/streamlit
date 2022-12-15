import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

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

geyser = pd.read_csv("oldfaithful.csv")

col1, col2 = st.columns([1,3])

with col1:
    clust_num = st.slider('Clusters', 1, 272)
    kmModel = KMeans(n_clusters = clust_num)
    kmModel = kmModel.fit(geyser)
    centroids = kmModel.cluster_centers_
    clusters = kmModel.fit_predict(geyser[['Eruption', 'Waiting']])

with col2:
    fig, ax = plt.subplots()
    sns.scatterplot(data=geyser, x='Eruption', y='Waiting', hue=clusters, style=clusters)
    ax.get_legend().remove()
    ax.set_xlabel('Eruption time (min)', fontsize=14)
    ax.set_ylabel('Waiting time (min)', fontsize=14)
    st.pyplot(fig)