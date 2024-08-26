import streamlit as st
from auth.auth_handler import register_user
from utils.utils import countries

def show_signup_page():
    st.title("Sign Up")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    country = st.selectbox("Country", countries)
    
    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match")
        else:
            success, message = register_user(username, password, country)
            if success:
                st.success(message)
                st.session_state['page'] = 'signin'
                st.rerun()
            else:
                st.error(message)
