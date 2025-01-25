import streamlit as st
import requests
import json
import re

st.title("User Registration")

# Collect user input
first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
school = st.text_input("School")
birthday = st.date_input("Birthday")
gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Other"])

required_fields = [first_name, last_name, email, password, school, birthday, gender]

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# Submit button
if st.button("Register"):
    if all(required_fields):
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
        else:
            user_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,  # In a real application, hash the password before sending
                "school": school,
                "birthday": birthday.isoformat(),
                "gender": gender,
                "house_id": None,
                "swipes": [],
                "profile_picture": None,
                "images": []
                }

            # Send the data to the backend
            response = requests.post("http://127.0.0.1:5000/add_user", json=user_data)

            if response.status_code == 201:
                st.success("User registered successfully!")
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    else:
        st.error("Please fill out all required fields.")
