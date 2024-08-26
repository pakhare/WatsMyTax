import streamlit as st
from auth.auth_handler import authenticate_user

def show_signin_page():
    st.title("Sign In")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        success, message = authenticate_user(username, password)
        if success:
            st.success("Signed in successfully")
            st.session_state['page'] = 'dashboard'
            st.rerun()
        else:
            st.error(message)

    st.write("Don't have an account?")
    if st.button("Go to Sign Up"):
        st.session_state['page'] = 'signup'
        st.rerun()
