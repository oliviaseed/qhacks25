import streamlit as st


# logo
# st.image()
st.markdown("<h1 style='text-align: center;'>RoomieU</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Find your perfect housemate!</p>", unsafe_allow_html=True)
st.divider()

st.markdown(
    """
    <style>
    .centered-button {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Wrap buttons in a div with the centered class
st.markdown('<div class="centered-button">', unsafe_allow_html=True)
if st.button("Click Me"):
    st.write("Button Clicked!")
st.markdown('</div>', unsafe_allow_html=True)

# Top nav bar
with st.container():
    col1, col2, col3 = st.columns(3, gap="small",vertical_alignment="center")
    with col1:
        st.button(" ", icon=":material/person:")

    with col2:
        st.button(" ", icon=":material/home:")

    with col3:
        st.button(" ", icon=":material/chat_bubble:")
    

# profiles
main_container = st.container(border=True)

with main_container:
    col1, col2 = st.columns(2, vertical_alignment="center")
    with col1:
        with st.container():
            st.markdown("""
                <div style='border: 1px solid; padding: 20px; width: 100%; height: 100%;'>
                    <img src='nia.jpg' style='width: 100%; height: auto;' />
                    <p>Location</p>
                    <h3 style='text-align: center;'>Nia Engineering Undergrad</h3>
                </div>
            """, unsafe_allow_html=True)
    with col2:
        with st.container(border=True):
            st.markdown("""
                <div style='text-align: center;'>
                    <h2>About You</h2>
                </div>
            """, unsafe_allow_html=True)
        # TODO: put user's information
        with st.container():
                st.write("Bio")    
            


# Create columns for the yes and no buttons
col5, col6 = st.columns(2, gap="small",vertical_alignment="center")

# Place yes and no buttons in columns
with col5:
    st.button(" ", icon=":material/cancel:")

with col6:
    st.button(" ", icon=":material/check_circle:")




import streamlit as st
from PIL import Image


def main():
    st.set_page_config(page_title="RoomieU", layout="wide")

    # Title
    st.markdown("<h1 style='text-align: center;'>RoomieU</h1>", unsafe_allow_html=True)

   
    
    

    # Navigation links with page_link
    st.markdown(
        """
        <div style='text-align: center;'>
            {home_link} {chat_link} {profile_link}
        </div>
        """.format(
            home_link=st.page_link("home.py", label="Home", icon=":material/home:"),
            chat_link=st.page_link("pages/chat.py", label="Chat", icon=":material/chat_bubble:"),
            profile_link=st.page_link("pages/profile.py", label="Profile", icon=":material/account_circle:")
        ),
        unsafe_allow_html=True,
    )


    st.write("### Find your perfect housemate!")

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
            


def display_chat():
    st.write("## Chat")
    st.write("Chat with your potential roommates here.")
    # Chat implementation can be expanded as needed


def display_profile():
    st.write("## Profile")
    st.write("Update and view your profile details here.")
    # Profile editing feature can be added


if __name__ == "__main__":
    main()



