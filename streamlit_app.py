import requests
import streamlit as st
from country_list import countries_for_language

# IBM IAM Token Endpoint and Watsonx.ai API details
IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"
API_URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"


# Obtain IAM token using API Key
def get_iam_token(api_key):
    response = requests.post(
        IAM_TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": api_key,
        },
    )
    if response.status_code != 200:
        st.error("Error obtaining IAM token")
        return None
    return response.json().get("access_token")


# Get tax strategy from IBM Watsonx.ai API
def get_tax_strategy(data, iam_token):
    body = {
        "input": f"""
            Generate a personalized tax-saving strategy for a user based on their financial profile. 
            Assume the numbers to be in Local Currency.
            Input:  
                Country: {data['country']}
                Earnings: {data['earnings']}
                Tax: {data['tax']}
                Investment: {data['investment']}
                Deductions: {data['deductions']}

            Respond with a structured tax-saving strategy for the user. The text output should be well formatted and easy to understand.
        """,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 1000,
            "repetition_penalty": 1,
        },
        "model_id": "ibm/granite-13b-chat-v2",
        "project_id": st.secrets["project"]["id"],
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {iam_token}",
    }
    response = requests.post(API_URL, headers=headers, json=body)
    if response.status_code != 200:
        st.error("Error fetching data from the API")
        return None

    response_json = response.json()
    results = response_json.get("results", [])
    if results:
        return results[0].get("generated_text", "No strategy found")
    return "No strategy found"


def display_form():
    st.title("🧾 Tax Optimization Strategy 🏦")

    # Read API Key from Streamlit secrets
    api_key = st.secrets["api"]["key"]

    st.sidebar.header("User Information")

    # Get the list of countries
    countries = [country[1] for country in countries_for_language("en")]

    # Form Fields
    country = st.sidebar.selectbox("Country", countries)
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
        "Monthly Investments (Local Currency)", min_value=0, step=100
    )
    deductions = st.sidebar.number_input(
        "Deductions (Local Currency)", min_value=0, step=100
    )
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
        iam_token = get_iam_token(api_key)
        if iam_token:
            strategy = get_tax_strategy(data, iam_token)
            if strategy:
                st.write("**Personalized Tax-Saving Strategy:**")
                st.write(strategy)


if __name__ == "__main__":
    display_form()
