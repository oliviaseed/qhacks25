import streamlit as st
from src.utils.db import get_mongo_db
from src.utils.auth import authenticate_user, set_cookies, clear_cookies, logout
from streamlit_cookies_manager import EncryptedCookieManager
from bson import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize cookies manager with password
cookie_password = os.getenv("COOKIE_PASSWORD")
if not cookie_password:
    st.error("COOKIE_PASSWORD environment variable not set.")
    st.stop()

cookies = EncryptedCookieManager(password=cookie_password)
if not cookies.ready():
    st.stop()

db = get_mongo_db()
users_collection = db["users"]

# Check if user is already logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

# Check cookies for login state
if cookies.get("logged_in") == "true":
    user_id = cookies.get("user_id")
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        st.session_state.logged_in = True
        st.session_state.user = user

# Placeholder for login status
login_status = st.empty()

if st.session_state.logged_in:
    st.success(f"Welcome {st.session_state.user['first_name']}!")
    st.write('You are now logged in.')
    if st.button("Logout"):
        logout()
        st.rerun()  # Refresh the page to show the logged-out state
else:
    # User input for login
        email = st.text_input('Email:')
        password = st.text_input('Password:', type='password')
        if st.button('Login'):
            user = authenticate_user(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                set_cookies(user)
                login_status.success('Login successful!')
                st.rerun()  # Refresh the page to show the logged-in state
            else:
                login_status.error('Invalid email or password. Please try again.')
