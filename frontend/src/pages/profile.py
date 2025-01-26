import streamlit as st
from PIL import Image
import requests
import json
from src.utils.auth import setup_auth
from bson import ObjectId
import base64
import time

def encode_img(image_file):
    try:
        return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


cookies, db, login_status = setup_auth()
# timeout = 10  # seconds
# start_time = time.time()
# while not cookies.ready():
#     if time.time() - start_time > timeout:
#         st.error("Cookies manager not ready. Please try again later.")
#         st.stop()
#     time.sleep(0.1)
users_collection = db["users"]
houses_collection = db["houses"]

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

# Function to update user data
def update_house(house_id, data):
    url = f"http://127.0.0.1:5000/update_house/{house_id}"
    headers = {"Content-Type": "application/json"}
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    return response

def create_house(user_id, data):
    url = f"http://127.0.0.1:5000/add_house/{user_id}"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response

# Function to upload image
def upload_image(file):
    url = "http://127.0.0.1:5000/upload_image"
    files = {'file': (file.name, file.getvalue(), file.type)}
    response = requests.post(url, files=files)
    return response

def upload_images(images):
    encoded_images = []
    for uploaded_file in images:
        response = upload_image(uploaded_file)
        if response.status_code == 200:
            try:
                response_json = response.json()
                file_path = response_json.get("file_path")
                encoded_images.append(file_path)
            except requests.exceptions.JSONDecodeError:
                st.error("Error uploading image: Invalid JSON response")
        else:
            st.error(f"Error uploading image: {response.content.decode('utf-8')}")
    return encoded_images

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
        if personal_images:
            cols = st.columns(len(personal_images))
            for i, img_file in enumerate(personal_images):
                with cols[i]:
                    img = Image.open(img_file)
                    st.image(img, use_column_width=True)

    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        st.session_state.logged_in = True
        st.session_state.user = user
    # Housing Section
    with col2:
        st.subheader("Housing Information")
        house_id = st.session_state.user.get("house_id", "")
        house = houses_collection.find_one({"_id": ObjectId(house_id)})
        if house is None:
            house = {}
        rent = st.text_input("Rent ($)", value=house.get("rent", "-"))
        utilities_included = st.checkbox("Utilities Included", value=house.get("utilities_included", False))
        rooms_available = st.text_input("Rooms Available", value=house.get("rooms_available", "1"))
        bathrooms = st.text_input("Bathrooms", value=house.get("bathrooms", "1"))
        address = st.text_input("Address", value=house.get("address", ""))
        city = st.text_input("City", value=house.get("city", ""))
        province = st.text_input("Province", value=house.get("province", ""))
        lease_length = st.text_input("Lease Length (months)", value=house.get("lease_length", "12"))
        available_from = st.date_input("Available From", value=house.get("available_from", None))
        house_type = st.selectbox(
            "House Type",
            ["House", "Apartment", "Studio"],
            index=["House", "Apartment", "Studio"].index(
                house.get("house_type", "Apartment")
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
        user_data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "school": school,
            "bio": bio,
        }

        house_data = {
            "house_type": house_type,
            "rooms_available": rooms_available,
            "rent": rent,
            "utilities_included": utilities_included,
            "bathrooms": bathrooms,
            "address": address,
            "city": city,
            "province": province,
            "lease_length": lease_length,
            "available_from": available_from.isoformat() if available_from else None,
        }
        # Handle image uploads
        if personal_images:
            images = upload_images(personal_images)
            user_data["images"] = images
        if housing_images:
            images = upload_images(housing_images)
            house_data["images"] = images
            print("TEST!!:)")

        # Remove empty fields from the data
        user_data = {k: v for k, v in user_data.items() if v}
        response = update_user(user_id, user_data)
        if response.status_code == 200:
            st.success("Profile updated successfully!")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
        
        house_data = {k: v for k, v in house_data.items() if v}
        if house_data and house_id:
            response = update_house(house_id, house_data)
            if response.status_code == 200:
                st.success("House updated successfully!")
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
        elif house_data:
            response = create_house(user_id, house_data)
            if response.status_code == 200:
                st.success("House created successfully!")
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")

else:
    st.error("You must log in to access the profile page.")
