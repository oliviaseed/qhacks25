import streamlit as st
import hashlib
from src.utils.db import get_mongo_db
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

db = get_mongo_db()
users_collection = db["users"]

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to authenticate user
def authenticate_user(email, password):
    email = email.strip()  # Remove leading/trailing whitespace
    user = users_collection.find_one({"email": email})
    if user and user["password"] == password:
    # if user and user["password"] == hash_password(password):
        return user
    return None

# Function to set cookies
def set_cookies(user):
    cookies["logged_in"] = "true"
    cookies["user_id"] = str(user["_id"])
    cookies.save()

# Function to clear cookies
def clear_cookies():
    cookies["logged_in"] = "false"
    cookies["user_id"] = ""
    cookies.save()

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

# User input for login
email = st.text_input('Email:')
password = st.text_input('Password:', type='password')

# Placeholder for login status
login_status = st.empty()

if st.session_state.logged_in:
    st.success(f"Welcome {st.session_state.user['first_name']}!")
    st.write('You are now logged in.')
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        clear_cookies()
        st.rerun()
else:
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