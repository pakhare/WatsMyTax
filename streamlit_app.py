import os

import requests
import streamlit as st
from langchain_ibm import WatsonxLLM
from auth.signin import show_signin_page
from auth.signup import show_signup_page
from middleware.auth_middleware import auth_middleware
from auth.auth_handler import getAuthenticatedUser
from utils.utils import countries


os.environ["WATSONX_APIKEY"] = st.secrets["api"]["key"]
# IBM Watsonx.ai details
MODEL = "ibm/granite-13b-chat-v2"
API_URL = "https://us-south.ml.cloud.ibm.com"


# Get tax strategy from IBM Watsonx.ai API
def generate_tax_strategy(data):
    prompt = f"""
            Generate a personalized tax-saving strategy for a user based on their financial profile. 
            Assume the numbers to be in Local Currency.
            Input:  
                Country: {data['country']}
                Earnings: {data['earnings']}
                Tax: {data['tax']}
                Investment: {data['investment']}
                Deductions: {data['deductions']}
                {data['additional_info']}

            Respond with a structured tax-saving strategy for the user. 
            The text output should contain the calculation between before & after-tax income.
            It also should be well formatted (numbered/bulleted/paragraphs/formulae) and easy to understand.
            Make sure to use currency symbols (Example $, €, etc) and percentages where necessary.
        """

    watsonx_llm = WatsonxLLM(
        model_id=MODEL,
        project_id=st.secrets["project"]["id"],
        url=API_URL,
        params={
            "decoding_method": "greedy",
            "max_new_tokens": 1000,
            "repetition_penalty": 1,
        },
    )
    st.write_stream(watsonx_llm.stream(prompt))


def display_form():
    st.title("🧾 Tax Optimization Strategy 🏦")

    st.sidebar.header("User Information")
    if st.sidebar.button("Sign Out"):
            st.session_state['authenticated'] = False
            st.session_state['page'] = 'signin'
            st.rerun()

    auth_user = getAuthenticatedUser()

    # Form Fields
    country = st.sidebar.selectbox("Country", countries, index=countries.index(auth_user['country']) if auth_user else 0)
    earnings = st.sidebar.number_input(
        "Monthly Earnings (Local Currency)",
        min_value=0,
        max_value=1000000,
        value=5000,
        step=500,
    )
    tax = st.sidebar.slider(
        "Current Tax Rate (%)", min_value=0, max_value=100, value=30, step=1
    )
    investment = st.sidebar.number_input(
        "Monthly Investments (Local Currency)", min_value=0, value=100, step=100
    )
    deductions = st.sidebar.slider(
        "Deductions (%)", min_value=0, max_value=100, value=None, step=1
    )

    if earnings is None:
        st.sidebar.error("Please enter your monthly earnings.")
    if tax is None:
        st.sidebar.error("Please set the current tax rate.")
    if investment is None:
        st.sidebar.error("Please enter your monthly investments.")
    if deductions is None:
        st.sidebar.error("Please enter your deductions.")

    if all(
        [
            earnings is not None,
            tax is not None,
            investment is not None,
            deductions is not None,
        ]
    ):
        st.write("All required inputs are provided.")

    additional_info = st.sidebar.text_area("Additional Information")

    if st.sidebar.button("Submit"):
        data = {
            "country": country,
            "earnings": earnings,
            "tax": tax,
            "investment": investment,
            "deductions": deductions,
            "additional_info": additional_info,
        }
        try:
            generate_tax_strategy(data)
        except Exception as e:
            st.error(f"Error: {e}")

def main():
    # Initialize session state for page navigation
    if 'page' not in st.session_state:
        st.session_state['page'] = 'signin'

    # Page routing
    if st.session_state['page'] == 'signin':
        show_signin_page()
    elif st.session_state['page'] == 'signup':
        show_signup_page()
    else:
        auth_middleware()   # Apply middleware to check authentication - 
                            # Will redirect automatically to signup if not authenticated
        # st.title("Dashboard")
        # st.write(f"Welcome, {st.session_state['username']}!")
        display_form()


if __name__ == "__main__":
    main()
