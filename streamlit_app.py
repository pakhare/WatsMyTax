import json
import os
from typing import Iterable

import streamlit as st
from langchain_core.messages.ai import AIMessageChunk
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableGenerator
from langchain_ibm import WatsonxLLM

from auth.auth_handler import delete_user, getAuthenticatedUser
from auth.signin import show_signin_page
from auth.signup import show_signup_page
from middleware.auth_middleware import auth_middleware
from utils.utils import countries

st.set_page_config(
    page_title="WatsMyTax",
    page_icon="https://raw.githubusercontent.com/pakhare/WatsMyTax/main/mytax.ico",
)

os.environ["WATSONX_APIKEY"] = st.secrets["api"]["key"]
# IBM Watsonx.ai details
MODEL = "ibm/granite-13b-chat-v2"
API_URL = "https://us-south.ml.cloud.ibm.com"


def generate_tax_expressions(data):
    task_prompt = """
        Generate a personalized tax-saving calculations for a user based on their financial profile. 
        The result should only be a list of JSON objects containing the following fields:

        expression: The calculation expression (the numbers with arithmetic operations).
        description: The arithmetic description of the calculation in plain English.
        currency: The currency symbol used in the calculation for the country. Should change for different countries.

        Example Input:
            Country: India
            Earnings: 500000 per month
            Tax: 10%
            Investment: 100000 per month
            Deductions: 20000
            Additional Information: The user is a salaried employee.
        
        Example raw JSON output (these formulas are just examples and may not be accurate, the length of the list can vary):
        [
            {
                "expression": "500000 * 0.10",
                "description": "Tax Amount = Income Bracket * Tax Rate",
                "currency": "₹"
            },
            {
                "expression": "500000 - (500000 * 0.10)",
                "description": "After Tax Income = Income Bracket - Tax Amount",
                "currency": "₹"
            }
        ]
    """
    prompt = f"""
        Input:  
            Country: {data["country"]}
            Earnings: {data["earnings"]} per month
            Tax: {data["tax"]}%
            Investment: {data["investment"]} per month
            Deductions: {data["deductions"]}
            Additional Information: {data["additional_info"]}

        Now, ONLY generate the list of JSONs as instructed above using the input and nothing else. 
        Do not explain anything and do not share codes just provide the JSON output.
    """
    prompt = task_prompt + prompt

    watsonx_llm = WatsonxLLM(
        model_id="ibm/granite-13b-instruct-v2",
        project_id=st.secrets["project"]["id"],
        url="https://us-south.ml.cloud.ibm.com",
        params={
            "decoding_method": "greedy",
            "max_new_tokens": 1000,
            "repetition_penalty": 1,
        },
    )

    response = watsonx_llm.generate([prompt])
    text = response.generations[0][0].text
    print(text)

    text = text[text.find("[") : text.find("]") + 1]
    res_dict = json.loads(text)
    for d in res_dict:
        try:
            d["result"] = eval(d["expression"])
        except:
            d["result"] = "No result available"

    result = [
        r["description"] + " = " + r["expression"] + " = " + str(r["result"])
        for r in res_dict
    ]
    result = "\n".join(result)
    print(result)
    return result


def streaming_parse(chunks: Iterable[AIMessageChunk]) -> Iterable[str]:
    for chunk in chunks:
        # Replace $ with \$
        modified_content = chunk.replace("$", r"\$")
        yield modified_content


# Get tax strategy from IBM Watsonx.ai API
def generate_tax_strategy(data):
    tax_results = generate_tax_expressions(data)

    prompt = """
            Generate a personalized tax-saving strategy for a user based on their financial profile. 
            
            Input:  
                Country: {country}
                Earnings: {earnings} per month
                Tax: {tax}%
                Investment: {investment} per month
                Deductions: {deductions}
                Additional Information: {additional_info}

            Here are the tax-saving calculations for the user:
            {tax_results}
            Assume local currency.
            First, show me and explain to me these calculations.
            Then, provide a tax-saving strategy beyond these calculations as well.
            Make sure the results are well formatted (numbered, bulleted, formulae, etc) and easy to understand for the user 
            and don't change paragraphs and use escape characters where needed (ex. dollar symbol).
        """

    chat_prompt = PromptTemplate.from_template(template=prompt)
    chat_prompt = chat_prompt.format(
        country=data["country"],
        earnings=data["earnings"],
        tax=data["tax"],
        investment=data["investment"],
        deductions=data["deductions"],
        additional_info=data["additional_info"],
        tax_results=tax_results,
    )

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
    streaming_parser = RunnableGenerator(streaming_parse)
    watsonx_llm = watsonx_llm | StrOutputParser() | streaming_parser
    st.write_stream(watsonx_llm.stream(chat_prompt))


def display_form():
    st.title("WatsMyTax 🧾")

    st.sidebar.header("User Information")

    auth_user = getAuthenticatedUser()

    # Form Fields
    country = st.sidebar.selectbox(
        "Country",
        countries,
        index=countries.index(auth_user["country"]) if auth_user else 0,
    )
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

    output_placeholder = st.empty()

    # Initial placeholder message in the main area
    with output_placeholder.container():
        st.markdown("### Start Optimizing Your Taxes!")
        st.write(
            """
            Fill in the form on the left with your financial details to receive a customized tax-saving strategy.
            Our AI-powered tool will analyze your inputs and provide you with actionable strategies to minimize your tax burden.
        """
        )
        st.image(
            "https://i.imgur.com/ARAt4O6.png",
            caption="Optimize Your Taxes",
            use_column_width=True,
        )

    if st.sidebar.button("Submit"):
        data = {
            "country": country,
            "earnings": earnings,
            "tax": tax,
            "investment": investment,
            "deductions": deductions,
            "additional_info": additional_info,
        }
        output_placeholder.empty()
        try:
            generate_tax_strategy(data)
        except Exception as e:
            st.error(f"Error: {e}")
    
    if st.sidebar.button("Sign Out"):
        st.session_state['authenticated'] = False
        st.session_state['page'] = 'signin'
        st.rerun()
    
    if st.sidebar.button("Delete Account", help="This will delete your account and all associated data.", type="primary"):
            delete_user(st.session_state['user']['username'])
            st.session_state['page'] = 'signin'
            st.rerun()


def main():
    # Initialize session state for page navigation
    if "page" not in st.session_state:
        st.session_state["page"] = "signin"

    # Page routing
    if st.session_state["page"] == "signin":
        show_signin_page()
    elif st.session_state["page"] == "signup":
        show_signup_page()
    else:
        auth_middleware()  # Apply middleware to check authentication -
        # Will redirect automatically to signup if not authenticated
        # st.title("Dashboard")
        # st.write(f"Welcome, {st.session_state['username']}!")
        display_form()


if __name__ == "__main__":
    main()
