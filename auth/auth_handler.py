import streamlit as st
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(input_password, stored_password_hash):
    return hash_password(input_password) == stored_password_hash

def register_user(username, password, country):
    users = st.session_state.get('users', {})
    if username in users:
        return False, "Username already exists"
    users[username] = hash_password(password)
    users['country'] = country
    st.session_state['users'] = users
    return True, "User registered successfully"

def authenticate_user(username, password):
    users = st.session_state.get('users', {})
    if username in users and verify_password(password, users[username]):
        st.session_state['authenticated'] = True
        st.session_state['user'] = {
            "username": users[username],
            "country": users['country'],
        }
        return True, "Authenticated successfully"
    return False, "Invalid username or password"

def logout_user():
    st.session_state['authenticated'] = False
    st.session_state['username'] = None

def getAuthenticatedUser():
    return st.session_state.get('user', None)
