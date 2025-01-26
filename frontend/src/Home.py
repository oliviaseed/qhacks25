import streamlit as st
import sys
import os
from PIL import Image
from src.utils.auth import setup_auth
from src.utils.db import fetch_users
from src.utils.misc import calculate_age
from bson.objectid import ObjectId
import requests
from io import BytesIO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "frontend", "src")))

st.set_page_config(page_title="RoomieU", layout="wide")

cookies, db, login_status = setup_auth()
users_collection = db["users"]

# Check if user is logged in
if st.session_state.get('logged_in', False):
    st.title(f"Welcome, {st.session_state.user['first_name']}!")
    # st.write("This is your dashboard.")
    # if st.button("Logout"):
    #     logout()
    #     st.rerun()
else:
    st.switch_page("login.py")
    # st.title("Welcome to the App")
    # st.write("Please log in or register using the sidebar.")

user_id = cookies.get("user_id", [None])

current_page = st.query_params.get("page", ["Home"])[0]

if current_page == "Home":
    st.query_params.update({"page": "home"})
elif current_page == "Login":
    st.query_params.update({"page": "login"})
elif current_page == "Register":
    st.query_params.update({"page": "register"})
elif current_page == "Profile":
    st.query_params.update({"page": "profile"})

def swipe(user_id, target_user_id, action):
    url = "http://127.0.0.1:5000/swipe"
    data = {
        "user_id": user_id,
        "target_user_id": target_user_id,
        "action": action
    }
    response = requests.post(url, json=data)
    return response

def get_profile_picture(user_id):
    url = f"http://127.0.0.1:5000/view_user_image/{user_id}/0"
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        st.error("Error fetching profile picture")
        return None
    
def render_page():
    # Apply custom CSS for styling
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <style>
        body {
            background-color: #FAFAF9;
        }
        .header {
            text-align: center;
            padding: 15px 0;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .icons {
            display: flex;
            justify-content: center;
            gap: 40px;
        }
        .icon {
            cursor: pointer;
            font-size: 24px;
            color: #333333;
        }
        .icon:hover {
            color: #6FB3B8;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Static content for this placeholder file
    st.markdown("<h3 style='text-align: center;'>Find your perfect housemate!</h3>", unsafe_allow_html=True)


    # Header with navigation icons
    st.markdown(
        f"""
        <div class="header">
            <div class="icons">
                <span class="icon" onclick="window.location.href='chat.py';">
                    <span class="material-icons">chat</span>
                </span>
                <span class="icon" onclick="window.location.href='home.py';">
                    <span class="material-icons">home</span>
                </span>
                <span class="icon" onclick="window.location.href='profile.py';">
                    <span class="material-icons">person</span>
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if user_id:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        #others
        target_users = fetch_users(user_id)
        target = target_users[0]
        # Get the current user based on the user index

        # Profile Section
        profile_col1, profile_col2 = st.columns([1, 2])

        # Add a sample profile picture
        with profile_col1:
            st.write(f"### **{target['first_name']} {target['last_name']}**")
            profile_pic = target.get("images", [None])[0]
            if profile_pic:
                profile_pic = get_profile_picture(target["_id"])
                st.image(profile_pic, use_container_width=True)

        # Add user bio
        birthday = target.get("birthday", "N/A")
        age = calculate_age(birthday) if birthday != "N/A" else "N/A"
        with profile_col2:
            st.write(f""" 
            **Age:** {age}                               
            **Gender:** {target.get("gender", "N/A")}  
            **University:** {target.get('school', 'N/A')}  
            **Bio:** {target.get('bio', 'N/A')}
            """)

        # Swipe buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("", icon=":material/cancel:"):
                swipe(user_id, target["_id"], "dislike")
                target_users.pop(0)
                st.rerun()
        with col3:
            if st.button("", icon=":material/check_circle:"):
                swipe(user_id, target["_id"], "like")
                target_users.pop(0)
                st.rerun()

        # Check if there are no more users left
        if 0 >= len(target_users):
            st.write("No more users left.")

    else:
        st.error("You must log in to access the profile page.")

    # Bottom buttons
    st.markdown("---")


def main():

    # Title
    st.markdown("<h1 style='text-align: center;'>RoomieU</h1>", unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FAFAF9;
        }
        .stButton>button {
            background-color: #6FB3B8;
            color: #333333;
        }
        .stButton>button:hover {
            background-color: #5F9DA3;
        }
        .feature-section {
            background-color: #E5EAF0;
            padding: 20px;
            border-radius: 10px;
        }
        h1, h2, h3, p, div, span {
            color: #333333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
    render_page()
