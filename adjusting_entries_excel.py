"""
This is a demo of the mitosheet library. It is a simple streamlit app that allows you to import data and clean it using mitosheet.
"""

import streamlit as st
import pandas as pd
from mitosheet.streamlit.v1 import spreadsheet

st.set_page_config(layout="wide")


col1, col2 = st.columns([2,3])

with col1:
    st.title("Adjusting Entries for Accruals")
    st.markdown("""
    This activity walks you through the steps of adjusting entries for accruals. To start the activity, click **Import** > **Import Files** and select journal.xlsx file from the `data` folder. Then, click the **Import Button**, and configure the import to skip rows depending on the file you choose.

    Micro Computer Services Inc. began operations on August 1, 2025. At the end of August 2025, management attempted to prepare monthly financial statements. The following information relates to August.
    1. At August 31, the company owed its employees $800 in salaries that will be paid on September 1.
    2. On August 1, the company borrowed $30,000 from a local bank on a 1-year note payable. The annual interest rate is 10%. Interest will be paid with the note at maturity.
    3. Revenue for services performed but unrecorded for August totaled $1,100.

    Prepare the adjusting entries needed at August 31, 2025.
    """)


CHECKS_AND_ERRORS = [
    # First column is issue date
    (
        lambda df: df.iloc[0,0] != 'Salaries and Wages Expense',
        'Enter the account name for the adjusted entry being debited in Cell A2.',
        'You can do this by clicking the cell under Account name. Enclose the account name in double quotations and make sure that Edit entire column is set to Off.'
    ),

    (
        lambda df: df.iloc[0,1] != 800,
        'Enter the amount for the adjusted entry being debited in Cell B2.',
        'You can do this by clicking the cell under Account name. Type =, then the amount and make sure that Edit entire column is set to Off.'
    ),

    (
        lambda df: df.iloc[1,0] != 'Salaries and Wages Payable',
        'Enter the account name for the adjusted entry being debited in Cell A3.',
        'You can do this by clicking the cell under Account name. Enclose the account name in double quotations and make sure that Edit entire column is set to Off.'
    )
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
        st.success("That is the correct account!")
