import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

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

WBCD = pd.read_csv("WisconsinBreastCancerDatabase.csv")
WBCD.loc[WBCD['Diagnosis']=='B','Diagnosis']=0
WBCD.loc[WBCD['Diagnosis']=='M','Diagnosis']=1

# Store relevant columns as variables
X = WBCD[['Radius mean']].values.reshape(-1, 1)
y = WBCD[['Diagnosis']].values.reshape(-1, 1).astype(int)

#Logistic regression predicting diagnosis from tumor radius
logisticModel = LogisticRegression()
logisticModel.fit(X,np.ravel(y.astype(int)))

col1, col2 = st.columns([1,3])

with col1:
    threshold = st.slider('Threshold',0.0, 1.0, 0.1)
    yPredictedProb = logisticModel.predict_proba(X)[:,1]
    yPredLowCutoff = []
    for i in range(0,yPredictedProb.size):
        if yPredictedProb[i] < threshold:
            yPredLowCutoff.append(0)
        else:
            yPredLowCutoff.append(1)
    st.write("Accuracy: " + str(round(metrics.accuracy_score(y,yPredLowCutoff),2)))
    st.write("Precision: " + str(round(metrics.precision_score(y,yPredLowCutoff),2)))
    st.write("Recall: " + str(round(metrics.recall_score(y,yPredLowCutoff),2)))

with col2:
    #Graph logistic regression probabilities
    fig, ax = plt.subplots()
    x = [X.min(),X.max()]
    y_val = [threshold, threshold]
    x_val = (np.log(threshold/(1-threshold))+15.120902)/1.02475609
    plt.scatter(X,y)
    plt.plot(x, y_val, color='gray', linewidth=3)
    plt.plot([x_val,x_val],[0,1], color='gray', linewidth=3)
    xDelta = np.linspace(X.min(),X.max(),10000)
    yPredicted = logisticModel.predict(X).reshape(-1,1).astype(int)
    yDeltaProb = logisticModel.predict_proba(xDelta.reshape(-1,1))[:,1]
    plt.plot(xDelta,yDeltaProb, color='red')
    ax.set_xlabel('Radius mean',fontsize=14);
    ax.set_ylabel('Probability of malignant tumor',fontsize=14);
    st.pyplot(fig)
    desc1 = "Description: A classification model using logistic regression will "
    desc2 = "classify tumors with a radius mean of less than " + str(round(x_val,2))
    desc3 = " as benign. Tumors with a radius mean of "
    desc4 = "greater than or equal to " + str(round(x_val,2)) + "will be classified as malignant."
    st.write(desc1 + desc2 + desc3 + desc4)
