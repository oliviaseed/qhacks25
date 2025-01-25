import streamlit as st

# Page Layout
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

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

# Custom CSS for layout and chat bubbles
st.markdown(
    """
    <style>
    /* General layout styles */
    .block-container {
        padding: 0 !important;
    }
    /* Top bar with RoomieU */
    .top-bar {
        background-color: #1E1E1E;
        padding: 15px 20px;
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 1000;
        font-size: 1.5rem;
        font-weight: bold;
    }
    /* Button bar styles */
    .button-bar {
        background-color: #333;
        padding: 10px 20px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        position: fixed;
        top: 60px;
        left: 0;
        width: 100%;
        z-index: 999;
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
    /* Chat sidebar */
    .chat-sidebar {
        background-color: #1E1E1E;
        color: white;
        height: 100vh;
        overflow-y: auto;
        padding: 20px;
        width: 300px;
        position: fixed;
        top: 120px;
        left: 0;
    }
    .chat-sidebar h2 {
        margin-top: 0;
        padding-bottom: 10px;
        font-size: 1.2rem;
        border-bottom: 1px solid #333;
    }
    .chat-sidebar .match {
        padding: 15px;
        border: 1px solid #333;
        border-radius: 5px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }
    .chat-sidebar .match:hover {
        background-color: #333;
    }
    .chat-sidebar .match.selected {
        background-color: #444;
        font-weight: bold;
    }
    .chat-content {
        margin-left: 320px;
        padding: 20px;
        margin-top: 160px;
    }
    .chat-bubble {
        max-width: 60%;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 20px;
        line-height: 1.5;
    }
    .chat-bubble.user {
        background-color: #444;
        color: white;
        align-self: flex-end;
        text-align: right;
    }
    .chat-bubble.other {
        background-color: #333;
        color: white;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-top: 20px;
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

# Sidebar for Matches
matches = ["Nia", "John", "Emily", "Mother Stewart", "Yellow"]
selected_match = matches[0]  # Default selection is the first match

# Render Matches with Custom Styling
st.markdown(
    f"""
    <div class="chat-sidebar">
        <h2>Matches</h2>
        {''.join(f'<div class="match {"selected" if match == selected_match else ""}">{match}</div>' for match in matches)}
    </div>
    """,
    unsafe_allow_html=True,
)

# Chat Content
chat_messages = [
    {"sender": "Nia", "message": "Hi! How's your housemate search going?"},
    {"sender": "You", "message": "It's going well! How about you?"},
    {"sender": "Nia", "message": "I just found a great place!"},
]

# Dynamically generate and render chat bubbles
chat_html = """
<div class="chat-container">
"""
for msg in chat_messages:
    if msg["sender"] == "You":
        chat_html += f"""
        <div class="chat-bubble user">
            <p><strong></strong></p>
            <p>{msg['message']}</p>
        </div>
        """
    else:
        chat_html += f"""
        <div class="chat-bubble other">
            <p><strong>{msg['sender']}</strong></p>
            <p>{msg['message']}</p>
        </div>
        """
chat_html += "</div>"

# Display Chat Content
st.markdown(
    f"""
    <div class="chat-content">
        <h2>Chat with {selected_match}</h2>
        {chat_html}
    </div>
    """,
    unsafe_allow_html=True,
)
