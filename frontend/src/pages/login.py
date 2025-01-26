import streamlit as st
from src.utils.auth import setup_auth, authenticate_user, set_cookies, clear_cookies, logout

cookies, db, login_status = setup_auth()
users_collection = db["users"]

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

# Check if user is already logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

if st.session_state.logged_in:
    st.success(f"Welcome {st.session_state.user['first_name']}!")
    st.write('You are now logged in.')
    if st.button("Logout"):
        logout(cookies)
        st.rerun()  # Refresh the page to show the logged-out state
else:
    # User input for login
        email = st.text_input('Email:')
        password = st.text_input('Password:', type='password')
        if st.button('Login'):
            user = authenticate_user(email, password, users_collection)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                set_cookies(cookies, user)
                login_status.success('Login successful!')
                st.rerun()  # Refresh the page to show the logged-in state
            else:
                login_status.error('Invalid email or password. Please try again.')
