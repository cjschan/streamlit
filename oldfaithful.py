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
    clust_num = st.slider('Clusters', 1, 5)
    kmModel = KMeans(n_clusters = clust_num)
    kmModel = kmModel.fit(geyser)
    centroids = kmModel.cluster_centers_
    clusters = kmModel.fit_predict(geyser[['Eruption', 'Waiting']])
    st.write("WCSS = " + str(int(kmModel.inertia_)))

with col2:
    fig, ax = plt.subplots()
    sns.color_palette("viridis", as_cmap=True)
    sns.scatterplot(data=geyser, x='Eruption', y='Waiting', hue=clusters, s=80, palette="colorblind")
    ax.get_legend().remove()
    ax.set_xlabel('Eruption time (min)', fontsize=14)
    ax.set_ylabel('Waiting time (min)', fontsize=14)
    x_cent = []
    y_cent = []
    for i in centroids:
        x_cent.append(i[0])
        y_cent.append(i[1])
    plt.scatter(x=x_cent, y=y_cent, c="black", marker="X", s=120)
    st.pyplot(fig)
    desc1 = "Description: A scatter plot of the Old Faithful eruption data"
    if clust_num==1
        desc2 = "with " + str(clust_num) + " cluster. The within-cluster sum of "
    else:
        desc2 = "with " + str(clust_num) + " clusters. The within-cluster sum of "
    desc3 = "squares is equal to " + str(int(kmModel.inertia_)) + "."
    desc = desc1 + desc2 + desc3
    st.write(desc)
