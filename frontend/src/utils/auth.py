import streamlit as st
import hashlib
from dotenv import load_dotenv
import os
from streamlit_cookies_manager import EncryptedCookieManager
from src.utils.db import get_mongo_db

db = get_mongo_db()
users_collection = db["users"]

# Load environment variables from .env file
load_dotenv()

# Initialize cookies manager with password
cookie_password = os.getenv("COOKIE_PASSWORD")
if not cookie_password:
    st.error("COOKIE_PASSWORD environment variable not set.")
    st.stop()

cookies = EncryptedCookieManager(password=cookie_password)

# Function to check if the user is logged in
def check_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None

# Function to log in a user
def login(username, password):
    # Replace this with your own authentication logic (e.g., database check)
    if username == "admin" and password == "password":
        st.session_state.logged_in = True
        st.session_state.user = username
        return True
    else:
        return False

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    clear_cookies()

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