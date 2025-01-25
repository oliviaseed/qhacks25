import streamlit as st
from PIL import Image
import requests
import json
from src.utils.db import get_mongo_db
from streamlit_cookies_manager import EncryptedCookieManager
from bson import ObjectId
from dotenv import load_dotenv
import os
import base64

# Load environment variables from .env file
load_dotenv()

# Initialize cookies manager
cookie_password = os.getenv("COOKIE_PASSWORD")
if not cookie_password:
    st.error("COOKIE_PASSWORD environment variable not set.")
    st.stop()

cookies = EncryptedCookieManager(password=cookie_password)
if not cookies.ready():
    st.stop()

# Database connection
db = get_mongo_db()
users_collection = db["users"]

# Check login state
if cookies.get("logged_in") == "true":
    user_id = cookies.get("user_id")
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        st.session_state.logged_in = True
        st.session_state.user = user
    else:
        st.session_state.logged_in = False
        st.session_state.user = None
else:
    st.session_state.logged_in = False
    st.session_state.user = None

# Function to update user data
def update_user(user_id, data):
    url = f"http://127.0.0.1:5000/update_user/{user_id}"
    headers = {"Content-Type": "application/json"}
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    return response

# Function to upload image
def upload_image(file):
    url = "http://127.0.0.1:5000/upload_image"
    files = {'file': file}
    response = requests.post(url, files=files)
    return response

# Authentication and Profile Page
if st.session_state.logged_in:
    st.success(f"Welcome {st.session_state.user['first_name']}!")
    
    # Layout for Personal and Housing sections
    st.markdown('<div class="header">RoomieU - Profile Page</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    # Personal Section
    with col1:
        st.subheader("Personal Information")
        email = st.text_input("Email", value=st.session_state.user.get("email", ""))
        first_name = st.text_input("First Name", value=st.session_state.user.get("first_name", ""))
        last_name = st.text_input("Last Name", value=st.session_state.user.get("last_name", ""))
        school = st.text_input("School", value=st.session_state.user.get("school", ""))
        bio = st.text_area("Bio", value=st.session_state.user.get("bio", ""))

        st.markdown('<div class="custom-label">Upload Personal Pictures</div>', unsafe_allow_html=True)
        personal_images = st.file_uploader("", accept_multiple_files=True, key="personal_pics")
        # if personal_images:
        #     cols = st.columns(len(personal_images))
        #     for i, img_file in enumerate(personal_images):
        #         with cols[i]:
        #             img = Image.open(img_file)
        #             st.image(img, use_column_width=True)

    # Housing Section
    with col2:
        st.subheader("Housing Information")
        lease_length = st.selectbox(
            "Lease Length", 
            ["Short-term (1–6 months)", "Long-term (6+ months)", "Flexible"],
            index=["Short-term (1–6 months)", "Long-term (6+ months)", "Flexible"].index(
                st.session_state.user.get("housing_info", {}).get("lease_length", "Flexible")
            )
        )
        budget = st.text_input("Budget (Min-Max)", value=st.session_state.user.get("housing_info", {}).get("budget", ""))
        roommates_count = st.selectbox(
            "Number of Roommates",
            ["1", "2", "3+", "No Preference"],
            index=["1", "2", "3+", "No Preference"].index(
                st.session_state.user.get("housing_info", {}).get("roommates_count", "No Preference")
            )
        )
        house_type = st.selectbox(
            "House Type",
            ["House", "Apartment", "Studio"],
            index=["House", "Apartment", "Studio"].index(
                st.session_state.user.get("housing_info", {}).get("house_type", "Apartment")
            )
        )
        st.markdown('<div class="custom-label">Upload Housing Pictures</div>', unsafe_allow_html=True)
        housing_images = st.file_uploader("", accept_multiple_files=True, key="housing_pics")
        if housing_images:
            cols = st.columns(len(housing_images))
            for i, img_file in enumerate(housing_images):
                with cols[i]:
                    img = Image.open(img_file)
                    st.image(img, use_column_width=True)

    # Submit Button
    if st.button("Submit"):
        data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "school": school,
            "bio": bio,
            "housing_info": {
                "lease_length": lease_length,
                "budget": budget,
                "roommates_count": roommates_count,
                "house_type": house_type,
            }
        }
        # Handle image uploads
        if personal_images:
            images = []
            for uploaded_file in personal_images:
                response = upload_image(uploaded_file)
                if response.status_code == 200:
                    try:
                        response_json = response.json()
                        file_path = response_json.get("file_path")
                        images.append(file_path)
                    except requests.exceptions.JSONDecodeError:
                        st.error("Error uploading image: Invalid JSON response")
                else:
                    st.error(f"Error uploading image: {response.content.decode('utf-8')}")
            data["images"] = images

        # Remove empty fields from the data
        data = {k: v for k, v in data.items() if v}
        # print("data", data)
        response = update_user(user_id, data)
        if response.status_code == 200:
            st.success("Profile updated successfully!")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
else:
    st.error("You must log in to access the profile page.")
