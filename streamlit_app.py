# streamlit_app.py
import streamlit as st
import requests

# IBM Watsonx.ai API details
API_URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
# Access API key from Streamlit secrets
API_KEY = st.secrets["api"]["key"]

def get_tax_strategy(data):
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
        "Authorization": f"Bearer sKeQGQ6IsYI1kxERE12cLtXPGFN4Sn461TFTR75xkcym"
    }
    response = requests.post(API_URL, headers=headers, json=body)
    if response.status_code != 200:
        st.error("Error fetching data from the API")
        return None
    return response.json().get("output", "No strategy found")

def display_form():
    st.title("Tax Optimization Strategy")

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
        strategy = get_tax_strategy(data)
        if strategy:
            st.write("**Personalized Tax-Saving Strategy:**")
            st.write(strategy)

if __name__ == "__main__":
    display_form()
