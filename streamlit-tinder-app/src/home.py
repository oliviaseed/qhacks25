import streamlit as st
from st_clickable_images import clickable_images
# logo
# st.image()
st.title('RoomieU')
st.write('Find your perfect housemate!')
st.divider()

# Create columns for the buttons


# Place buttons in columns
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
    st.image("nia.jpg")
    main_container.write("Nia, Engineering Undergrad")





# Create columns for the yes and no buttons
col5, col6 = st.columns(2)

# Place yes and no buttons in columns
with col5:
    st.button(" ", icon=":material/cancel:")

with col6:
    st.button(" ", icon=":material/check_circle:")

st.divider()


