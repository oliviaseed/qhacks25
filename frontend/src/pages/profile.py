import streamlit as st
from PIL import Image

st.set_page_config(page_title="profile", layout="wide")

# Colors and styling
BACKGROUND_COLOR = "#FAFAF9"
HEADER_COLOR = "#B3CDE0"
BUTTON_COLOR = "#6FB3B8"
TEXT_COLOR = "#333333"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {BACKGROUND_COLOR};
    }}
    
    .header {{
        background-color: {HEADER_COLOR};
        padding: 0.5rem;
        border-radius: 8px;
        text-align: center;
        color: {TEXT_COLOR};
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }}
    
    .subheader {{
        color: {TEXT_COLOR};
        font-size: 1rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }}
    
    .custom-label {{
        font-size: 0.9rem;
        color: {TEXT_COLOR};
        margin-bottom: 0.3rem;
        font-weight: 500;
    }}
    
    .placeholder {{
        background-color: #D3D3D3;
        width: 100%;
        height: 150px;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: {TEXT_COLOR};
        border-radius: 8px;
        font-size: 0.9rem;
    }}
    
    .stSelectbox div[data-baseweb="select"],
    .stMultiSelect div[data-baseweb="select"] {{
        font-size: 0.85rem !important;
        padding: 0.2rem 0.5rem !important;
    }}
    
    .stNumberInput input,
    .stTextInput input,
    .stTextArea textarea {{
        font-size: 0.85rem !important;
        padding: 0.2rem 0.5rem !important;
    }}
    
    .stButton button {{
        font-size: 0.9rem !important;
        padding: 0.4rem 0.8rem !important;
        background-color: {BUTTON_COLOR};
        color: white;
        border: none;
        border-radius: 8px;
    }}
    
    .stSelectbox, .stNumberInput, .stTextInput, .stTextArea, .stRadio, .stMultiSelect {{
        margin-bottom: 1.5rem;
    }}

    .stNumberInput > div {{
        border: none !important; /* Remove the container border */
        background-color: transparent !important; /* Make the background transparent */
        box-shadow: none !important; /* Remove any shadow effect */
    }}

    .stNumberInput input {{
        border: none !important;
        box-shadow: none !important;
        outline: none !important; /* Remove the focus outline */
        background-color: transparent !important; /* Optional: Make the background transparent */
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

def custom_label(text):
    st.markdown(f'<div class="custom-label">{text}</div>', unsafe_allow_html=True)

# Header
st.markdown('<div class="header">RoomieU - Profile Page</div>', unsafe_allow_html=True)

# Layout
col1, col2 = st.columns(2, gap="medium")

# Personal Section
with col1:
    st.markdown('<div class="subheader">Personal Information</div>', unsafe_allow_html=True)
    
    custom_label("Upload Personal Pictures")
    personal_images = st.file_uploader("", accept_multiple_files=True, key="personal_pics")
    cols = st.columns(4)
    for i in range(4):
        with cols[i]:
            if personal_images and len(personal_images) > i:
                img = Image.open(personal_images[i])
                st.image(img, use_column_width=True)
            else:
                st.markdown(f'<div class="placeholder">+</div>', unsafe_allow_html=True)

    custom_label("What best describes your situation?")
    st.selectbox("", ["Looking for a Housemate", "Listing My House/Sublet"], key="housemate_option")
    
    custom_label("Gender")
    st.selectbox("", ["Male", "Female", "Nonbinary", "Other"], key="gender")
    
    custom_label("Age")
    st.number_input("", min_value=0, max_value=150, key="age")
    
    custom_label("School, Program, Graduation Year")
    st.text_input("", key="school_program_year")
    
    custom_label("Cleanliness Level")
    st.selectbox(
        "",
        ["Always Clean", "Mostly Clean", "Casual", "Flexible"],
        key="cleanliness_level"
    )
    
    custom_label("Schedule Preference")
    st.selectbox("", ["Early Bird", "Night Owl", "Flexible"], key="schedule_preference")
    
    custom_label("Personality Type")
    st.selectbox("", ["Introvert", "Extrovert", "Ambivert"], key="personality_type")
    
    custom_label("Confrontation Style")
    st.selectbox("", ["Let's Talk About It", "Depends on What It Is", "I Keep Quiet"], key="confrontation_style")
    
    custom_label("Pets")
    st.multiselect("", ["Cat", "Dog", "No Preference", "Don't Like", "Allergic to Pets"], key="pets_preference")
    
    custom_label("Interests/Hobbies")
    st.text_area("", key="hobbies")

# Housing Section
with col2:
    st.markdown('<div class="subheader">Housing Information</div>', unsafe_allow_html=True)
    
    custom_label("Upload Housing Pictures")
    housing_images = st.file_uploader("", accept_multiple_files=True, key="housing_pics")
    cols = st.columns(4)
    for i in range(4):
        with cols[i]:
            if housing_images and len(housing_images) > i:
                img = Image.open(housing_images[i])
                st.image(img, use_column_width=True)
            else:
                st.markdown(f'<div class="placeholder">+</div>', unsafe_allow_html=True)

    custom_label("Lease Length")
    st.selectbox("", ["Short-term (1–6 months)", "Long-term (6+ months)", "Flexible"], key="lease_length")
    
    custom_label("Budget (Min-Max)")
    st.text_input("", key="budget")
    
    custom_label("Number of Roommates")
    st.selectbox("", ["1", "2", "3+", "No Preference"], key="roommates_count")
    
    custom_label("School Distance")
    st.selectbox("", ["On-campus", "Walking Distance", "Public Transport Accessible"], key="school_distance")
    
    custom_label("House Type")
    st.selectbox("", ["House", "Apartment", "Studio"], key="house_type")
    
    custom_label("Furnished Status")
    st.selectbox("", ["Fully Furnished", "Partially Furnished", "Unfurnished"], key="furnished_status")
    
    custom_label("Number of Rooms")
    st.number_input("", min_value=0, key="rooms_count")
    
    custom_label("Number of Bathrooms")
    st.number_input("", min_value=0, key="bathrooms_count")
    
    custom_label("Parking")
    st.selectbox("", ["Yes", "No", "Limited"], key="parking")
    
    custom_label("Utilities Included")
    st.selectbox("", ["Yes", "No", "Partially"], key="utilities_included")
    
    custom_label("Laundry")
    st.selectbox("", ["In-Unit", "Shared", "No Laundry"], key="laundry")
    
    custom_label("Dishwasher")
    st.selectbox("", ["Yes", "No"], key="dishwasher")
    
    custom_label("Heating")
    st.selectbox("", ["Yes", "No"], key="heating")
    
    custom_label("Air Conditioning (A/C)")
    st.selectbox("", ["Yes", "No"], key="ac")
