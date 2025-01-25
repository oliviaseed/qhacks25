import streamlit as st
import requests

def get_user_matches(user_id):
    try:
        response = requests.get(f"http://127.0.0.1:5000/matches/{user_id}")
        response.raise_for_status()
        return response.json()  # Assuming the API returns JSON
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching matches: {e}")
        return []
    
def get_user_info(user_id):
    """Fetch user information using their user ID."""
    try:
        response = requests.get(f"http://127.0.0.1:5000/get_user/{user_id}")
        response.raise_for_status()
        return response.json()  # Assuming the API returns JSON
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching user info: {e}")
        return {"first_name": "Unknown", "last_name": "Unknown"}

# Page Layout
st.set_page_config(layout="wide")

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

# Custom CSS for layout and match list
st.markdown(
    """
    <style>
    /* Title and button bar */
    .top-bar {
        background-color: #1E1E1E;
        padding: 15px 20px;
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .button-bar {
        background-color: #333;
        padding: 10px 20px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin-bottom: 20px;
    }
    .button-bar button {
        background-color: #444;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1rem;
    }
    .button-bar button:hover {
        background-color: #555;
    }
    /* Match list styles */
    .match-name {
        font-weight: bold;
        font-size: 1rem;
        margin-bottom: 5px;
    }
    .match-message {
        font-size: 0.9rem;
        color: gray;
    }
    .custom-button {

        width: 25%;
        text-align: left;
        background-color: blue;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 8px;
        border: 1px solid #ddd;
        font-size: 1rem;
        font-family: Arial, sans-serif;
        cursor: pointer;
    }
    .custom-button:hover {
        background-color: #f0f0f0;
    }
    .custom-button .name {
        font-weight: bold;
        font-size: 1rem;
        margin-bottom: 5px;
    }
    .custom-button .message {
        font-size: 0.9rem;
        color: gray;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Top Bar
st.markdown(
    """
    <div class="top-bar">
        RoomieU
    </div>
    """,
    unsafe_allow_html=True,
)

# Button Bar
st.markdown(
    """
    <div class="button-bar">
        <button>Profile</button>
        <button>Home</button>
        <button>Chat</button>
    </div>
    """,
    unsafe_allow_html=True,
)


user_id = "679551b210c72c24d160e32a"  # Example User ID

# Fetch matches
matches_data = get_user_matches(user_id)

# Ensure matches is extracted from the response
if isinstance(matches_data, dict) and "matches" in matches_data:
    matches = matches_data["matches"]
else:
    st.error("Unexpected data format from the matches API.")
    matches = []

# Display matches
if matches:
    st.header("Matches")
    for match in matches:
        # Extract relevant data
        user2_id = (
            match["user2_id"] if match["user1_id"] == user_id else match["user1_id"]
        )
        last_message = match.get("last_message", {})
        last_message_text = last_message.get("message", "No messages yet.")

        # Fetch user info for user2_id
        user_info = get_user_info(user2_id)
        first_name = user_info.get("first_name", "Unknown")
        last_name = user_info.get("last_name", "User")
        match_name = f"{first_name} {last_name}"

        # Render match as a clickable button
        if st.markdown(
            f"""
            <button class="custom-button" onclick="alert('Clicked {match_name}')">
                <div class="name">{match_name}</div>
                <div class="message">{last_message_text}</div>
            </button>
            """,
            unsafe_allow_html=True,
        ):
            continue
else:
    st.markdown("<p>No matches found. Start connecting today!</p>", unsafe_allow_html=True)
