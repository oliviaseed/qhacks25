import streamlit as st
from PIL import Image

st.set_page_config(page_title="RoomieU - Profile Page", layout="wide", page_icon="🏠")

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
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        color: {TEXT_COLOR};
        font-size: 7rem;  /* Doubled from 3.5rem */
        font-weight: bold;
        margin-bottom: 3rem;  /* Increased for better spacing */
    }}
    
    .subheader {{
        color: {TEXT_COLOR};
        font-size: 4rem;  /* Doubled from 2rem */
        font-weight: 600;
        margin: 2rem 0;
    }}
    
    /* Form element styling */
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {{
        font-size: 36px !important;  /* Doubled from 18px */
    }}
    
    .stRadio label,
    .stRadio div {{
        font-size: 36px !important;  /* Doubled from 18px */
    }}
    
    .stNumberInput input,
    .stTextInput input,
    .stTextArea textarea {{
        font-size: 36px !important;  /* Doubled from 18px */
        line-height: 1.5 !important;
    }}
    
    div[data-baseweb="multiselect"] span,
    div[data-baseweb="multiselect"] div {{
        font-size: 36px !important;  /* Doubled from 18px */
    }}
    
    .custom-label {{
        font-size: 40px;  /* Doubled from 20px */
        color: {TEXT_COLOR};
        margin: 1.5rem 0 1rem 0;  /* Increased for better spacing */
        font-weight: 500;
    }}
    
    .placeholder {{
        background-color: #D3D3D3;
        width: 350px;
        height: 350px;
        display: inline-block;
        margin: 5px;
        text-align: center;
        line-height: 350px;
        color: {TEXT_COLOR};
        font-size: 4rem;  /* Doubled from 2rem */
    }}
    
    /* Upload button styling */
    .uploadedFile {{
        font-size: 32px !important;  /* Doubled from 16px */
    }}
    
    .stButton button {{
        font-size: 36px !important;  /* Doubled from 18px */
        padding: 1rem 2rem !important;  /* Increased padding for better button sizing */
    }}

    /* Uniform height for all form elements */
    .stSelectbox > div,
    .stMultiSelect > div,
    .stNumberInput > div,
    .stTextInput > div {{
        min-height: 80px !important;
    }}

    /* Target the inner containers */
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stNumberInput > div > div,
    .stTextInput > div > div {{
        min-height: 80px !important;
        height: 80px !important;
    }}

    /* Target the actual input elements */
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div,
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {{
        min-height: 80px !important;
        height: 80px !important;
        padding: 0.5rem !important;
    }}

    /* Radio button height consistency */
    .stRadio > div {{
        padding: 0.5rem !important;
        min-height: 80px !important;
    }}

    /* Special handling for select dropdowns to align content */
    .stSelectbox [data-baseweb="select"] > div:first-child,
    .stMultiSelect [data-baseweb="select"] > div:first-child {{
        height: 80px !important;
        min-height: 80px !important;
        display: flex !important;
        align-items: center !important;
    }}

    /* Keep text area (Interests/Hobbies) different */
    .stTextArea textarea {{
        min-height: 150px !important;
    }}

    /* Streamlit markdown text */
    .css-10trblm {{
        font-size: 36px !important;
    }}

    /* Streamlit default text */
    .css-1dp5vir {{
        font-size: 36px !important;
    }}

    /* File uploader text */
    .css-1x8cf1d {{
        font-size: 36px !important;
    }}

    /* Additional elements */
    p, span, div {{
        font-size: 36px !important;
    }}

    /* Increase spacing between form elements */
    .stSelectbox, .stNumberInput, .stTextInput, .stTextArea, .stRadio, .stMultiSelect {{
        margin-bottom: 2rem !important;
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
    cols = st.columns(4, gap="small")
    for i in range(4):
        with cols[i]:
            if personal_images and len(personal_images) > i:
                img = Image.open(personal_images[i])
                st.image(img, width=350)
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
        ["Always Clean: Shared spaces should always be tidy.",
         "Mostly Clean: Some clutter is fine, but no mess.",
         "Casual: A bit of mess is okay in shared spaces.",
         "Flexible: I can adapt to others' preferences."],
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
    cols = st.columns(4, gap="small")
    for i in range(4):
        with cols[i]:
            if housing_images and len(housing_images) > i:
                img = Image.open(housing_images[i])
                st.image(img, width=350)
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
