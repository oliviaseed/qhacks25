import streamlit as st
import requests

# Function to test
def get_user_info(user_id):
    """Fetch user information using their user ID."""
    try:
        response = requests.get(f"http://127.0.0.1:5000/get_user/{user_id}")
        response.raise_for_status()
        return response.json()  # Assuming the API returns JSON
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching user info: {e}")
        return {"name": "Unknown"}

def get_user_matches(user_id):
    try:
        response = requests.get(f"http://127.0.0.1:5000/matches/{user_id}")
        response.raise_for_status()
        return response.json()  # Assuming the API returns JSON
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching matches: {e}")
        return []

# Call the function
user_id = "679551b210c72c24d160e32a"
match_id = "67948cfccd3a78361e4bed1f"
result = get_user_info(user_id)
result2 = get_user_matches(user_id)

# Print the output
print("Test Output:", result)
print("Test Output:", result2)


