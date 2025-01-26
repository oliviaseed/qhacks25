import streamlit as st
import requests
import re
from datetime import datetime, timedelta
from src.utils.auth import setup_auth

cookies, users_collection, login_status = setup_auth()

# Redirect to home page if already logged in
if cookies.get("logged_in") == "true":
    st.switch_page("home.py")

# Hide Streamlit default menu and footer
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("User Registration")

# Calculate the date range for the birth date input
today = datetime.today()
min_date = today - timedelta(days=27*365)  # 27 years ago
max_date = today - timedelta(days=17*365)  # 17 years ago

# Collect user input
first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
school = st.text_input("School")
birthday = st.date_input("Birthday", min_value=min_date, max_value=max_date)
gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Other"])

required_fields = {
    "First Name": first_name,
    "Last Name": last_name,
    "Email": email,
    "Password": password,
    "School": school,
    "Birthday": birthday,
    "Gender": gender,
}

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# Submit button
if st.button("Register"):

    missing_fields = [field_name for field_name, field_value in required_fields.items() if not field_value]

    if missing_fields:
        st.error(f"Please fill out all required fields: {', '.join(missing_fields)}")
    elif not is_valid_email(email):
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