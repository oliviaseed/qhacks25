import streamlit as st
import hashlib
from db import get_mongo_db

db = get_mongo_db()
users_collection = db["users"]

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User input for login
email = st.text_input('Email:')
password = st.text_input('Password:', type='password')

# Placeholder for login status
login_status = st.empty()

# Function to authenticate user
def authenticate_user(email, password):
    email = email.strip()  # Remove leading/trailing whitespace
    user = users_collection.find_one({"email": email})
    if user and user["password"] == password:
    # if user and user["password"] == hash_password(password):
        return user
    return None

# Check if user is already logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

if st.session_state.logged_in:
    st.success(f"Welcome {st.session_state.user['first_name']}!")
    st.write('You are now logged in.')
    # Add navigation or other actions here
else:
    if st.button('Login'):
        user = authenticate_user(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            login_status.success('Login successful!')
            st.query_params(logged_in="true")  # Refresh the page to show the logged-in state
        else:
            login_status.error('Invalid email or password. Please try again.')