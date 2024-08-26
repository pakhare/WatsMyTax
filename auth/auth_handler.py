from sqlalchemy.orm import Session
from database import User, get_db
import hashlib
import streamlit as st

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(input_password, stored_password_hash):
    return hash_password(input_password) == stored_password_hash

def register_user(user):
    db: Session = next(get_db())
    existing_user = db.query(User).filter(User.username == user["username"]).first()
    if existing_user:
        return False, "Username already exists"
    
    print(user)
    new_user = User(username=user["username"], password_hash=hash_password(user["password"]), country=user["country"], preferences="")
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return True, "User registered successfully"

def authenticate_user(username, password):
    db: Session = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.password_hash):
        st.session_state['authenticated'] = True
        st.session_state['user'] = {
            "user_id": user.id,
            "username": username,
            "country": user.country,
        }

        return True, "Authenticated successfully"
    return False, "Invalid username or password"

def delete_user(username):
    db: Session = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    if user:
        st.session_state['authenticated'] = False
        st.session_state['user'] = None
        db.delete(user)
        db.commit()
        return True, "User deleted successfully"
    return False, "User not found"

def logout_user():
    st.session_state['authenticated'] = False
    st.session_state['user'] = None

def getAuthenticatedUser():
    return st.session_state.get('user', None)
