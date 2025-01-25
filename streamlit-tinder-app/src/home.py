import streamlit as st
from st_clickable_images import clickable_images
# logo
st.title('RoomieU')
st.write('Find your perfect housemate!')
st.divider()
# Sidebar for navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ['Profile', 'Match', 'Chat', 'Settings'])

# image
with st.container():
    st.image("nia.jpg")


# backen function to execute matching button clicks
def clicked():
    pass

# yes and no buttons
st.button(" ", icon=":material/close:")

clicked_image = clickable_images(
    [
        "images\left.png",  # Replace with your image path
        "images\yes.png"  # Replace with your image path
    ],
    titles=["No", "Yes"],
    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    img_style={"margin": "10px", "height": "100px"}
)

if clicked_image == 0:
    clicked()
elif clicked_image == 1:
    clicked()


st.divider()
# page buttons
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    st.button('Profile')
    st.button('Match')
    st.button('Chat')
    st.button('Settings')
st.image("images\home.png")
st.image("images\chat.png")
st.image("images\match.png")
st.image("images\profile.png")
