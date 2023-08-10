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

crabs = pd.read_csv("crab-groups.csv")

crabs.columns = ["Site", "Latitude", "Sample size", "Mean length", "Min length", "Max length", "Stdev length","Median length","Date"]
crabs = crabs[["Site", "Date", "Sample size","Latitude","Mean length", "Min length", "Max length","Median length"]]

thisdict = {
  "Mean length": "mean fiddler crab length",
  "Min length": "minimum fiddler crab length",
  "Max length": "maximum fiddler crab length",
  "Median length": "median fiddler crab length"
}

tab1, tab2, tab3, tab4 = st.tabs(["Plot", "Data","Prediction", "Summary statistics"])

with tab1:
    col1, col2 = st.columns([1.5,3])

    with col1:
        target = st.selectbox(
            "Select target feature",
            [
                "Mean length",
                "Min length",
                "Max length",
                "Median length"
            ]
        )

        # Store relevant columns as variables
        X = crabs[['Latitude']].values.reshape(-1, 1)
        y = crabs[[target]].values.reshape(-1, 1)

        # Logistic regression predicting diagnosis from tumor radius
        linearModel = LinearRegression()
        linearModel.fit(X,np.ravel(y.astype(float)))

        # regModeleq = st.checkbox("Display regression equation")
        add_reg = st.checkbox("Add regression line")
        add_resid = st.checkbox("Add residuals", disabled=(not add_reg))
        add_mean = st.checkbox("Add mean")

        m, b = np.polyfit(np.ravel(X).astype(float), np.ravel(y).astype(float), 1)
        m = np.round(m,3)
        b = np.round(b,3)

    with col2:
        fig, ax = plt.subplots()
        sns.scatterplot(x="Latitude", y=target, data=crabs)
        if add_reg:
            plt.plot([X.min(),X.max()],[m*X.min()+b, m*X.max()+b,], color="red",label="Regression line")
            plt.legend()
        ax.set_xlabel("Latitude", fontsize=14)
        ax.set_ylabel(target, fontsize=14)

        if add_mean:
            plt.axhline(y=y.mean() , color='darkorange', linewidth=2, label="Mean", linestyle=':')
            plt.legend()

        if add_resid:
            n = len(X)
            for i in range(len(X)):
                plt.plot([X[i],X[i]],[y[i],m*X[i]+b],color='grey',linewidth = 2)

        st.subheader("Plot")
        st.pyplot(fig)

        desc1 = "Description: Samples of fiddler crabs from 13 locations were taken and the " + thisdict[target]
        desc2 = " from each location was recorded. As the latitude increases, the " + thisdict[target]
        desc3 = " also increases."
        description = desc1 + desc2 + desc3
        st.write(description)
        if add_reg:
            st.write("The equation for the regression line is ")
            st.latex("\widehat{\\text{" + target + "}} = " + str(m) + "(\\text{Latitude})" + str(b) + ".")
        if add_mean:
            st.write("The mean of the target feature is ")
            st.latex("\overline{\\text{" + target + "}} = " + str(np.round(crabs[target].mean(),2))+ ".")

with tab2:
    st.table(crabs[["Site","Date","Sample size","Latitude",target]])

with tab3:
    st.subheader("Regression equation")
    st.latex("\widehat{\\text{" + target + "}} = " + str(m) + "(\\text{Latitude})" + str(b))
    st.subheader("Prediction")
    pred_text = "Move slider to find the predicted " + thisdict[target] + " when the latitude is"
    predictor = st.slider(pred_text,30.0, 43.0, 30.0, 0.1)
    prediction = np.round(m*predictor+b,2)
    st.latex("\widehat{\\text{" + target + "}} (" + str(predictor) + ") = " + str(m) + "(" + str(predictor) + ")" + str(b) + " = " + str(prediction))

with tab4:
    st.subheader("Summary statistics")
    st.table(crabs[["Latitude",target]].describe().T)
    st.subheader("Sum of squared errors")
    yPredicted = m*X + b
    SSEreg = np.round(sum((y - yPredicted)**2)[0],2)
    SSEyBar = np.round(sum((y - np.mean(y))**2)[0],2)
    ss_desc1 = "The sum of squared errors for the mean of the " + thisdict[target] + " is " + str(SSEyBar) + ". "
    ss_desc2 = "The sum of squared errors for the least squares regression line is " + str(SSEreg) + ". "
    ss_desc = ss_desc1 + ss_desc2
    st.write(ss_desc)
    st.subheader("Correlation coefficient")
    corr = np.round(np.corrcoef(crabs["Latitude"], crabs[target])[0,1],2)
    st.write("The correlation coefficient between latitude and " + thisdict[target] + " is " + str(corr) + ", which implies a strong positive correlation. ")
    st.write("The coefficient of determination is " + str(corr**2) + ", which means that " + str(corr**2*100) + "% of the variance in " + thisdict[target] + " can be explained by the variation in latitude using the least squares regression line.")
