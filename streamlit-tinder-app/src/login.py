import streamlit as st
# from utils.matching import swipe_users

st.title('RoomieU')
st.write('Find your perfect housemate!')
st.divider()
# Sidebar for navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ['Profile', 'Match', 'Chat', 'Settings'])

# User input for login
username = st.text_input('Username:')
password = st.text_input('Password:', type='password')

# Placeholder for login status
login_status = st.empty()

# Sample user credentials for demonstration
sample_username = 'user1'
sample_password = 'password123'

if st.button('Login'):
    if username == sample_username and password == sample_password:
        login_status.success('Login successful!')
        st.write('Welcome to House Tinder!')
        # Redirect to the main app page or perform other actions
    else:
        login_status.error('Invalid username or password. Please try again.')

