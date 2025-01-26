import streamlit as st
from pathlib import Path
from PIL import Image

# Define navigation links to different Python files
NAVIGATION = {
    "home": "home.py",
    "chat": "pages/chat.py",
    "profile": "pages/profile.py",
}

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

    
    # Profile Section
    
    profile_col1, profile_col2 = st.columns([1, 2])

    # Add a sample profile picture
    with profile_col1:
        profile_pic = Image.open("nia.jpg")  # Replace with actual profile pic path
        st.image(profile_pic, use_container_width=True)
        st.write("### **Name,** **Program**")

    # Add user bio
    with profile_col2:
        st.write("""
        **Age:** 25  
        **Interests:** Music, Hiking, Tech  
        **Bio:** Hi! I'm John, looking for a roommate who shares similar interests and loves adventure.
        """)



    # Bottom buttons
    st.markdown("---")
    bottom_col1, bottom_col2  = st.columns([1, 1])
    with bottom_col1:
        if st.button(" ", icon=":material/cancel:"):
            st.warning("You passed [Name].")
    with bottom_col2:
        if st.button(" ", icon=":material/check_circle:"):
            st.success("You matched with [Name]!")


def main():
    # st.set_page_config(page_title="RoomieU", layout="wide")

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
