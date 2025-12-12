import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Spotlight AI - Profile",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .profile-header {
        background: linear-gradient(135deg, #f44336 0%, #c62828 100%);
        padding: 3rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .stat-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border: 2px solid #e9ecef;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #f44336;
    }
    .stat-label {
        color: #6c757d;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {'email': 'firstlast@email.com', 'name': 'First Last'}
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {
        'dietary': [],
        'price_range': [1, 4],
        'noise_preference': 'Any',
        'cuisine_preferences': [],
        'location': 'San Jose, CA',
        'liked_places': [],
        'search_history': []
    }

# Profile Header
st.markdown(f"""
<div class="profile-header">
    <div style="font-size: 4rem; margin-bottom: 1rem;">👤</div>
    <h1 style="margin: 0;">{st.session_state.user_data['name']}</h1>
    <p style="font-size: 1.1rem; margin: 0.5rem 0;">✉️ {st.session_state.user_data['email']}</p>
    <p style="opacity: 0.9;">Member since January 2024</p>
</div>
""", unsafe_allow_html=True)

# Account Information
st.markdown("## Account Information")

# Profile Picture Placeholder
st.markdown("""
<div class="profile-picture">
    👤
    <!-- Replace this div with: <img src="your-image-url.jpg" alt="Profile Picture"> -->
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name", value=st.session_state.user_data['name'])
    email = st.text_input("Email Address", value=st.session_state.user_data['email'])

with col2:
    st.text_input("Password", value="••••••••", type="password", disabled=True)
    if st.button("Change Password"):
        st.info("Password change functionality coming soon!")


