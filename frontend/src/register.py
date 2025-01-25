import streamlit as st
import requests
import json

st.title("User Registration")

# Collect user input
first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
school = st.text_input("School")
age = st.number_input("Age", min_value=0, max_value=120, step=1)
gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Other"])
bio = st.text_area("Bio")
profile_picture = st.file_uploader("Profile Picture", type=["jpg", "jpeg", "png"])

# Submit button
if st.button("Register"):
    if first_name and last_name and email and password and school and age and gender and bio:
        # Prepare the data
        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,  # In a real application, hash the password before sending
            "school": school,
            "age": age,
            "gender": gender,
            "bio": bio,
            "is_listing": False,
            "house_id": None,
            "swipes": [],
            "profile_picture": None,
            "images": []
        }

        # Handle profile picture upload
        if profile_picture is not None:
            user_data["profile_picture"] = profile_picture.read()

        # Send the data to the backend
        response = requests.post("http://127.0.0.1:5000/add_user", json=user_data)

        if response.status_code == 201:
            st.success("User registered successfully!")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    else:
        st.error("Please fill out all fields.")