import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridOptionsBuilder, ColumnsAutoSizeMode
from st_aggrid.shared import GridUpdateMode

st.set_page_config(
    layout="centered"
)

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

# st.header("Manipulating the country dataset")
# instructions = "Clicking Filters "
# col_ins = "Click Columns to display specific columns in the country dataset."
# row_ins = "Click Filters to display rows that satisfy a specific condition. "
# row_ex1 = "Ex: Clicking Population and selecting less than and typing 1000000 "
# row_ex2 = "returns rows where the population column is less than 1000000."
# piv1 = "Toggling Pivot Mode under Columns calculates various summary "
# piv2 = "statistics such as average population of countries in each continent."

# st.write(row_ins + row_ex1 + row_ex2)
# st.write(col_ins)
# st.write(piv1 + piv2)


def aggrid_interactive_table(df: pd.DataFrame):
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        height=400,
        gridOptions=options.build(),
        theme="alpine",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
    )

    return selection


country = pd.read_csv(
    "country_complete.csv"
)
country=country[["Country","Continent","Years","Fertility","Emissions","Internet"]]

selection = aggrid_interactive_table(df=country)
