"""
This is a demo of the mitosheet library. It is a simple streamlit app that allows you to import data and clean it using mitosheet.
"""

import streamlit as st
import pandas as pd
from mitosheet.streamlit.v1 import spreadsheet

st.set_page_config(layout="wide")


col1, col2 = st.columns([2,3])

with col1:
    st.title("Data Cleaning Verification")
    st.markdown("""
    This app only allows you to download data after it passes a series of data quality checks. After importing data, the app will run a series of checks against your data and prompt you with a set of data cleaning steps.

    To use the app, follow the mitosheet below:
    1. Click **Import** > **Import Files** and select an XLSX file from the `data` folder.
    2. Click the **Import Button**, and configure the import to skip rows depending on the file you choose.
    3. Use the Mitosheet to clean the data according to the prompts.
    4. Once all of the checks pass, download the csv file.
    """)


CHECKS_AND_ERRORS = [
    # First column is issue date
    (
        lambda df: df.columns[0] != 'issue date',
        'Please edit the first column name to "issue date".',
        'You can do this by double clicking on the column name.'
    ),
    # Correct dtype
    (
        lambda df: df["issue date"].dtype != "datetime64[ns]",
        'Please change the dtype of the "issue date" column to datetime.',
        'You can do this by clicking on the Filter icon, and then selecting "datetime" from the "dtype" dropdown.'

    ),
    # No null values
    (
        lambda df: df["issue date"].isnull().sum() > 0,
        'Please filter out all null values from the issue date column.',
        'You can do this by clicking on the filter icon in the issue date column header, and adding an "Is Not Empty" filter.'
    ),
    # Delete the Notes column
    (
        lambda df: "Notes" in df.columns,
        'Please delete the "Notes" column, which is the final column of the dataframe.',
        'You can do this by selecting the column header and pressing the Delete key.'
    ),
    # Turn the term column into a number with the formula =VALUE(LEFT(term, 3))
    (
        lambda df: df["term"].dtype != "int64",
        'Please extract the number of months from the "term" column.',
        'To do so, double click on a cell in the column, and write the formula `=INT(LEFT(term, 3))`.'
    ),
]

with col2:
    def run_data_checks_and_display_prompts(df):
        """
        Runs the data checks and displays prompts for the user to fix the data.
        """
        for check, error_message, help in CHECKS_AND_ERRORS:
            if check(df):
                st.error(error_message + " " + help)
                return False
        return True

    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    # Display the data inside of the spreadsheet so the user can easily fix data quality issues.
    dfs, _ = spreadsheet(import_folder='./data')

    # If the user has not yet imported data, prompt them to do so.
    if len(dfs) == 0:
        st.info("Please import a file to begin. Click **Import** > **Import Files** and select a file from the `data` folder.")

        # Don't run the rest of the app if the user hasn't imported data.
        st.stop()

    # Run the checks on the data and display prompts
    df = list(dfs.values())[0]
    checks_passed = run_data_checks_and_display_prompts(df)

    # If the data passes all checks, allow the user to download the data
    if checks_passed:
        st.success("All checks passed! This data is clean, and ready to be downloaded.")

        csv = convert_df(df)

        st.download_button(
            "Press to Download",
            csv,
            "mito_verified_data.csv",
            "text/csv",
            key='download-csv'
        )
