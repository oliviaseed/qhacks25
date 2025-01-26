import streamlit as st

# Page Layout must be set first
st.set_page_config(layout="wide")

import requests
import json
import time
# from streamlit_autorefresh import st_autorefresh
import openai
from dotenv import load_dotenv
import os
from src.utils.auth import setup_auth
from bson import ObjectId
# # Periodic update for chat
# POLLING_INTERVAL = 30  # seconds



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

# Set OpenAI API key and organization
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG")

def generate_icebreakers(prompt, max_results=1):
    """
    Use OpenAI API to generate unique icebreaker suggestions.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if needed
            messages=[
                {"role": "system", "content": "Please provide three fun and interesting icebreakers or questions"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            n=max_results,  # Generate multiple responses
        )
        # Extract suggestions and remove duplicates
        suggestions = list(
            set(choice["message"]["content"].strip() for choice in response.choices)
        )
        return suggestions
    except Exception as e:
        st.error(f"Error generating icebreakers: {e}")
        return []



#API CALLS TO BACKEND
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
    
def get_chat_history(match_id):
    """Fetch user information using their user ID."""
    try:
        response = requests.get(f"http://127.0.0.1:5000/get_messages/{match_id}")
        response.raise_for_status()
        return response.json()  # Assuming the API returns JSON
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching user info: {e}")
        return {"first_name": "Unknown", "last_name": "Unknown"}
    

def send_message(match_id, sender_id, receiver_id, message):
    url = "http://127.0.0.1:5000/send_message"
    payload = {
        "match_id": match_id,
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "message": message,
    }
    try:
        response = requests.post(
            url, headers={"Content-Type": "application/json"}, data=json.dumps(payload)
        )
        if response.status_code == 200:
            st.success("Message sent successfully!")
        else:
            st.error(f"Failed to send message. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")



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
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
    body {
        background-color: #FAFAF9;
    }
    /* Title and button bar */
    .top-bar {
        background-color: #B3CDE0;
        padding: 15px 20px;
        color: black;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .button-bar {
        background-color: #F7A399;
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
        width: 100%;
        text-align: left;
        background-color: #6FB3B8;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 8px;
        border: 1px solid #ddd;
        font-size: 1rem;
        font-family: Arial, sans-serif;
        cursor: pointer;
    }
    .custom-button:hover {
        background-color: #5F9DA3;
    }
    .custom-button .name {
        font-weight: bold;
        font-size: 1rem;
        margin-bottom: 5px;
        background-color: #6FB3B8;
    }
    .custom-button .message {
        font-size: 0.9rem;
        color: gray;
    }
    /* Chat UI styles */
    .chat-box {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #ddd;
        height: 400px;
        overflow-y: auto;
        margin-bottom: 10px;
    }
    .sender-bubble, .receiver-bubble {
        display: inline-block;
        max-width: 70%;
        padding: 10px;
        margin: 5px 0;
        border-radius: 15px;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    .sender-bubble {
        background-color: #DCF8C6; /* Light green */
        color: black;
        float: right;
        clear: both;
        text-align: left;
    }
    .receiver-bubble {
        background-color: #E1E1E1; /* Light gray */
        color: black;
        float: left;
        clear: both;
        text-align: left;
    }
    .bubble-text {
        margin-bottom: 5px;
    }
    .bubble-timestamp {
        font-size: 0.75rem;
        color: gray;
        text-align: right;
    }
    .header {
        text-align: center;
        padding: 15px 0;
        border-radius: 10px;
        margin-bottom: 20px;
        color: black;
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


# user_id = "679551b210c72c24d160e32a"  # Example User ID

# Fetch matches
matches_data = get_user_matches(user_id)

# Ensure matches is extracted from the response
if isinstance(matches_data, dict) and "matches" in matches_data:
    matches = matches_data["matches"]
else:
    st.error("Unexpected data format from the matches API.")
    matches = []

# Two-column layout
col1, col2 = st.columns([1, 3])  # 1/4 width for the first column, 3/4 for the second

# Column 1: Match Buttons
with col1:
    st.header("Matches")
    if matches:  # Check if there are any matches
        for match in matches:
        # Ensure match is a valid dictionary
            if isinstance(match, dict):
                # Determine match-related information
                user2_id = (
                    match.get("user2_id") if match.get("user1_id") == user_id else match.get("user1_id")
                )
                user_info = get_user_info(user2_id) if user2_id else {"first_name": "Unknown", "last_name": "Unknown"}
                first_name = user_info.get("first_name", "Unknown")
                last_name = user_info.get("last_name", "User")
                match_name = f"{first_name} {last_name}"

                # Safely get the last message text
                last_message = match.get("last_message") or {}  # Use an empty dictionary if None
                last_message_text = last_message.get("message", "No messages yet.")

                # Create a form for each match
                with st.form(key=f"form_{match.get('match_id', 'unknown')}"):
                    # Submit button for the match
                    if st.form_submit_button(match_name):
                        st.session_state["selected_match_id"] = match.get("match_id")
            else:
                st.warning("Unexpected match format detected.")
    else:
        st.markdown("<p>No matches found. Start connecting today!</p>", unsafe_allow_html=True)


# Initialize session state for messages
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = {}

if "latest_message_id" not in st.session_state:
    st.session_state["latest_message_id"] = {}

# Add a mechanism for auto-refresh using Streamlit session state
if "refresh_trigger" not in st.session_state:
    st.session_state["refresh_trigger"] = 0


# Column 2: Chat Window and Input
with col2:
    st.header("Chat")
    selected_match_id = st.session_state.get("selected_match_id")

    if selected_match_id:
        # Fetch chat history
        chat_history = get_chat_history(selected_match_id)
        messages = chat_history.get("messages", [])
        latest_message_id = st.session_state["latest_message_id"].get(selected_match_id)

        # Update session state with new messages if available
        new_messages = []
        for message in messages:
            if latest_message_id and message["message_id"] == latest_message_id:
                break
            new_messages.append(message)

        if new_messages:
            new_messages.reverse()
            if selected_match_id in st.session_state["chat_history"]:
                st.session_state["chat_history"][selected_match_id].extend(new_messages)
            else:
                st.session_state["chat_history"][selected_match_id] = new_messages

            st.session_state["latest_message_id"][selected_match_id] = new_messages[-1]["message_id"]

        # Get all messages from session state
        all_messages = st.session_state["chat_history"].get(selected_match_id, [])

        # Sort messages by timestamp
        all_messages.sort(key=lambda msg: msg["timestamp"])

        # Display chat bubbles
        if all_messages:
            chat_bubbles = ""
            for message in all_messages:
                sender_id = message["sender_id"]
                msg_text = message["message"]
                timestamp = message["timestamp"]
                is_sender = sender_id == user_id

                # Bubble styling and alignment
                bubble_class = "sender-bubble" if is_sender else "receiver-bubble"
                alignment = "right" if is_sender else "left"
                sender_label = "You" if is_sender else "Match"

                # Build bubble HTML
                chat_bubbles += f"""
                <div class="{bubble_class}" style="text-align: {alignment}; padding: 10px; border-radius: 15px; margin-bottom: 10px; display: inline-block; max-width: 70%;">
                    <div style="font-size: 0.75rem; color: gray; margin-bottom: 3px;">{sender_label}</div>
                    <div class="bubble-text">{msg_text}</div>
                    <div class="bubble-timestamp" style="font-size: 0.75rem; color: gray; text-align: right;">{timestamp}</div>
                </div>
                """
            # Render chat bubbles
            st.markdown(
                f"""
                <div class="chat-box" style="padding: 15px; border-radius: 8px; border: 1px solid #ddd; height: 400px; overflow-y: auto; margin-bottom: 10px;">
                    {chat_bubbles}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # Render a blank chat window if no messages
            st.markdown(
                """
                <div class="chat-box" style="padding: 15px; border-radius: 8px; border: 1px solid #ddd; height: 400px; overflow-y: auto; margin-bottom: 10px; display: flex; align-items: center; justify-content: center;">
                    <p style="color: gray;">No messages yet. Start the conversation!</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Input for new messages
        user_input = st.text_input("Type your message:", key=f"user_input_{selected_match_id}")
        if st.button("Send", key=f"send_button_{selected_match_id}"):
            if user_input.strip():
                # Determine receiver ID dynamically
                for match in matches:
                    if match["match_id"] == selected_match_id:
                        receiver_id = match["user2_id"] if match["user1_id"] == user_id else match["user1_id"]
                        break
                else:
                    st.error("Could not find the receiver ID for this match.")
                    receiver_id = None

                if receiver_id:
                    send_message(selected_match_id, user_id, receiver_id, user_input)
                else:
                    st.error("Failed to send message. Receiver ID is missing.")
            else:
                st.warning("Please enter a message before sending.")
    else:
        st.write("Select a match to view the chat.")


# After the chat column implementation...

# Icebreaker Suggestions Section
st.header("Need Icebreakers?")
icebreaker_prompt = "Suggest creative and fun icebreakers for people meeting for the first time in a chat."

if st.button("Get Icebreaker Suggestions"):
    with st.spinner("Generating suggestions..."):
        suggestions = generate_icebreakers(icebreaker_prompt)
    if suggestions:
        st.subheader("Here are some icebreakers:")
        for idx, suggestion in enumerate(suggestions, start=1):
            st.markdown(f"{suggestion}")
    else:
        st.warning("No suggestions were generated. Try again.")
