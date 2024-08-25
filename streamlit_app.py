# streamlit_app.py
import streamlit as st
import requests

# IBM IAM Token Endpoint and Watsonx.ai API details
IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"
API_URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

# Obtain IAM token using API Key
def get_iam_token(api_key):
    response = requests.post(
        IAM_TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": api_key}
    )
    if response.status_code != 200:
        st.error("Error obtaining IAM token")
        return None
    return response.json().get("access_token")

# Get tax strategy from IBM Watsonx.ai API
def get_tax_strategy(data, iam_token):
    body = {
        "input": f"Generate a personalized tax-saving strategy for a user based on their financial profile.\n\nInput:\nCountry: {data['country']}\nEarnings: {data['earnings']}\nTax: {data['tax']}\n\nOutput:",
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 200,
            "repetition_penalty": 1
        },
        "model_id": "ibm/granite-13b-chat-v2",
        "project_id": "11cdd86e-9f3e-4b33-8a1b-75871d4dde26"
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {iam_token}"
    }
    response = requests.post(API_URL, headers=headers, json=body)
    if response.status_code != 200:
        st.error("Error fetching data from the API")
        return None

    # Parse the response JSON
    response_json = response.json()

    # Extract the 'generated_text' from the 'results' list
    results = response_json.get("results", [])
    if results:
        return results[0].get("generated_text", "No strategy found")
    return "No strategy found"

def display_form():
    st.title("Tax Optimization Strategy")

    # Read API Key from Streamlit secrets
    api_key = st.secrets["api"]["key"]

    country = st.text_input("Country", "India")
    earnings = st.number_input("Monthly Earnings (INR)", min_value=0)
    tax = st.number_input("Current Tax Rate (%)", min_value=0, max_value=100)

    # Add more fields as needed based on the questions
    # ...

    if st.button("Submit"):
        data = {
            "country": country,
            "earnings": earnings,
            "tax": tax,
            # Include other form data here
        }
        iam_token = get_iam_token(api_key)
        if iam_token:
            strategy = get_tax_strategy(data, iam_token)
            if strategy:
                st.write("**Personalized Tax-Saving Strategy:**")
                st.write(strategy)

if __name__ == "__main__":
    display_form()
