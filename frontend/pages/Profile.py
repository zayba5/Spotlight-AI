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

    /* --- REMOVE STREAMLIT DEFAULT TOP HEADER --- */
    header[data-testid="stHeader"] {
        visibility: hidden !important;
        height: 0px !important;
    }

    /* --- FIXED TOP NAV BAR --- */
    .custom-top-nav {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 60px;
        background-color: #f44336 !important;
        border-bottom: 1px solid #e53935;
        display: flex;
        align-items: center;
        padding: 0 20px;
        z-index: 99999 !important;
    }

    .custom-top-nav img {
        height: 32px;
        margin-right: 16px;
        filter: brightness(0) invert(1);
    }

    .custom-top-nav .search-wrapper {
        position: relative;
        flex-grow: 1;
        max-width: 500px;
        margin-left: 0;
    }

    .custom-top-nav .search-wrapper::before {
        content: '🔍';
        position: absolute;
        left: 12px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 16px;
        z-index: 1;
        pointer-events: none;
        filter: brightness(0) invert(1);
    }

    .custom-top-nav input {
        width: 100%;
        height: 36px;
        border: none;
        border-radius: 18px;
        padding: 0 16px 0 40px;
        background: #fff;
        outline: none;
        font-size: 15px;
        color: #333;
    }

    .custom-top-nav input::placeholder {
        color: #999;
    }

    /* Navigation Icons Container in Top Bar */
    .nav-icons-top {
        display: flex;
        align-items: center;
        gap: 0;
        margin-left: auto;
        height: 60px;
    }

    .nav-icon-top {
        min-width: 112px;
        height: 56px;
        display: flex !important;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        cursor: pointer !important;
        transition: all 0.2s ease;
        font-size: 24px;
        background: transparent;
        border: none;
        padding: 0;
        margin: 0;
        position: relative;
        color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 8px;
        text-decoration: none !important;
        pointer-events: auto !important;
        z-index: 100000 !important;
    }

    .nav-icon-top:hover {
        background: rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 1) !important;
    }

    .nav-icon-top.active {
        color: rgba(255, 255, 255, 1) !important;
    }

    .nav-icon-top.active::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: calc(100% - 16px);
        height: 3px;
        background: rgba(255, 255, 255, 1);
        border-radius: 3px 3px 0 0;
    }

    .nav-icon-top i {
        font-size: 24px;
        pointer-events: none;
        color: inherit !important;
    }

    /* --- REMOVE ALL TOP SPACING FROM STREAMLIT --- */
    [data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
        margin-top: 30px !important;
    }

    [data-testid="stSidebar"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
    }

    /* Hide Streamlit's automatic sidebar navigation */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"],
    [data-testid="stSidebar"] nav,
    [data-testid="stSidebar"] [role="navigation"],
    [data-testid="stSidebar"] ul[data-testid*="nav"],
    [data-testid="stSidebar"] div[data-testid*="nav"],
    [data-testid="stSidebar"] > div > div:first-child nav,
    [data-testid="stSidebar"] > div > div:first-child ul {
        display: none !important;
        visibility: hidden !important;
    }

    /* Hide sidebar navigation links */
    [data-testid="stSidebar"] a[href*="Homepage"],
    [data-testid="stSidebar"] a[href*="History"],
    [data-testid="stSidebar"] a[href*="Maps"],
    [data-testid="stSidebar"] a[href*="Profile"],
    [data-testid="stSidebar"] a[href*="Settings"] {
        display: none !important;
        visibility: hidden !important;
    }

    .main .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* --- THE MISSING RULE (this one fixes your last gap!!) --- */
    .main > div:nth-child(1) {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

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


