import streamlit as st
import hashlib
from dotenv import load_dotenv
import os
from streamlit_cookies_manager import EncryptedCookieManager
from src.utils.db import get_mongo_db
import time
from bson import ObjectId

def setup_auth():
    # Load environment variables from .env file
    load_dotenv()

    # Initialize cookies manager with password
    cookie_password = os.getenv("COOKIE_PASSWORD")
    if not cookie_password:
        st.error("COOKIE_PASSWORD environment variable not set.")
        st.stop()

    cookies = EncryptedCookieManager(password=cookie_password)
    timeout = 10  # seconds
    start_time = time.time()
    while not cookies.ready():
        if time.time() - start_time > timeout:
            st.error("Cookies manager not ready. Please try again later.")
            st.stop()
        time.sleep(0.1)

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

    return cookies, db, login_status

def logout(cookies):
    st.session_state.logged_in = False
    st.session_state.user = None
    clear_cookies(cookies)

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to authenticate user
def authenticate_user(email, password, users_collection):
    email = email.strip()  # Remove leading/trailing whitespace
    user = users_collection.find_one({"email": email})
    if user and user["password"] == password:
    # if user and user["password"] == hash_password(password):
        return user
    return None

# Function to set cookies
def set_cookies(cookies, user):
    cookies["logged_in"] = "true"
    cookies["user_id"] = str(user["_id"])
    cookies.save()

# Function to clear cookies
def clear_cookies(cookies):
    cookies["logged_in"] = "false"
    cookies["user_id"] = ""
    cookies.save()
