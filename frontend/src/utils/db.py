from pymongo import MongoClient
import streamlit as st
from dotenv import load_dotenv
import os
import requests
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

@st.cache_resource
def get_mongo_db():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # 5-second timeout
    db = client[DB_NAME]
    return db

# Function to fetch users from the backend
def fetch_users(user_id):
    # curl -X GET "http://127.0.0.1:5000/get_users?user_id=679486f52cbb9e9a76e75104&age=25&gender=Male"

    url = f"http://127.0.0.1:5000/get_users?user_id={user_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching users")
        return []
    
def fetch_profile_picture(user_id):
    url = f"http://127.0.0.1:5000/view_profile_picture/{user_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        return None
