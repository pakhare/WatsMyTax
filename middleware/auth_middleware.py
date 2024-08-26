import streamlit as st

def auth_middleware():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        st.warning("Please sign in to access this page.")
        st.session_state['page'] = 'signin'
        st.rerun()
