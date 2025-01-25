import streamlit as st

st.title('My First Streamlit App')
st.write('Hello, welcome to my first Streamlit web app!')

# Add a text input widget
name = st.text_input('Enter your name:')

# Display the input text
if name:
    st.write(f'Hello, {name}!')