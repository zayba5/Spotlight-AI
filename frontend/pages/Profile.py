import streamlit as st
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="Spotlight AI - Profile",
    layout="wide"
)

# Top Navigation Bar (HTML + CSS) - Same as Homepage
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
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
        padding-top: 0 !important;
        margin-top: 30px !important;
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
    }

    /* --- THE MISSING RULE (this one fixes your last gap!!) --- */
    .main > div:nth-child(1) {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    .saved-card {
        border: 2px solid #667eea;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .history-item {
        border-left: 4px solid #667eea;
        padding: 15px;
        margin: 10px 0;
        background: #f8f9fa;
        border-radius: 0 8px 8px 0;
    }
    .feedback-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 12px;
        font-size: 12px;
        margin-right: 8px;
    }
    .badge-liked {
        background: #d4edda;
        color: #155724;
    }
    .badge-disliked {
        background: #f8d7da;
        color: #721c24;
    }
    .stat-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Determine current page for highlighting
current_file = os.path.basename(__file__)
if current_file == "Homepage.py":
    current_page_name = "homepage"
elif current_file == "History.py":
    current_page_name = "history"
elif current_file == "Maps.py":
    current_page_name = "maps"
elif current_file == "Profile.py":
    current_page_name = "profile"
elif current_file == "Settings.py":
    current_page_name = "settings"
else:
    current_page_name = current_file.replace(".py", "").lower()

# Check query params for page navigation - MUST BE FIRST
query_params = st.query_params
if 'nav' in query_params:
    nav_page = query_params['nav']
    current_file_name = os.path.basename(__file__)
    
    if nav_page == 'homepage':
        st.switch_page("../Homepage.py")
    elif nav_page == 'history':
        # Already on history page - clear the nav param
        if 'nav' in st.query_params:
            del st.query_params['nav']
    elif nav_page == 'maps' and current_file_name != "Maps.py":
        st.switch_page("Maps.py")
    elif nav_page == 'profile' and current_file_name != "Profile.py":
        st.switch_page("Profile.py")
    elif nav_page == 'settings' and current_file_name != "Settings.py":
        st.switch_page("Settings.py")

# Top Navigation Bar with Icons - Using anchor tags for direct navigation
nav_html = f"""
<div class="custom-top-nav">
    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/No_image_available_600_x_450.svg">
    <div class="search-wrapper">
        <input type="text" placeholder="Search Spotlight AI...">
    </div>
    <div class="nav-icons-top">
        <a href="/" target="_self" class="nav-icon-top {'active' if current_page_name == 'homepage' else ''}" 
           title="Homepage" style="text-decoration: none; display: flex; align-items: center; justify-content: center;">
            <i class="fas fa-home"></i>
        </a>
        <a href="/History" target="_self" class="nav-icon-top {'active' if current_page_name == 'history' else ''}" 
           title="History" style="text-decoration: none; display: flex; align-items: center; justify-content: center;">
            <i class="fas fa-history"></i>
        </a>
        <a href="/Maps" target="_self" class="nav-icon-top {'active' if current_page_name == 'maps' else ''}" 
           title="Maps" style="text-decoration: none; display: flex; align-items: center; justify-content: center;">
            <i class="fas fa-map-marked-alt"></i>
        </a>
        <a href="/Profile" target="_self" class="nav-icon-top {'active' if current_page_name == 'profile' else ''}" 
           title="Profile" style="text-decoration: none; display: flex; align-items: center; justify-content: center;">
            <i class="fas fa-user"></i>
        </a>
        <a href="/Settings" target="_self" class="nav-icon-top {'active' if current_page_name == 'settings' else ''}" 
           title="Settings" style="text-decoration: none; display: flex; align-items: center; justify-content: center;">
            <i class="fas fa-cog"></i>
        </a>
    </div>
</div>
"""
st.markdown(nav_html, unsafe_allow_html=True)

# No JavaScript needed - using anchor tags for direct navigation

# Hide Streamlit's automatic sidebar navigation with JavaScript
st.markdown("""
<script>
(function() {
    // Hide navigation elements in sidebar
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        // Hide nav elements
        const navElements = sidebar.querySelectorAll('nav, [role="navigation"], [data-testid*="nav"], ul, a[href*="Homepage"], a[href*="History"], a[href*="Maps"], a[href*="Profile"], a[href*="Settings"]');
        navElements.forEach(el => {
            if (el.textContent && (el.textContent.includes('Homepage') || el.textContent.includes('History') || el.textContent.includes('Maps') || el.textContent.includes('Profile') || el.textContent.includes('Settings'))) {
                if (!el.closest('[class*="Preferences"]')) {
                    el.style.display = 'none';
                    el.style.visibility = 'hidden';
                }
            }
        });
        
        // Also hide first child if it's navigation
        const firstChild = sidebar.querySelector('> div > div:first-child');
        if (firstChild && (firstChild.textContent.includes('Homepage') || firstChild.textContent.includes('History') || firstChild.textContent.includes('Maps'))) {
            firstChild.style.display = 'none';
        }
    }
    
    // Run again after a short delay to catch dynamically loaded elements
    setTimeout(() => {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            const navElements = sidebar.querySelectorAll('a, button, div');
            navElements.forEach(el => {
                const text = el.textContent || '';
                if ((text.includes('Homepage') || text.includes('History') || text.includes('Maps') || text.includes('Profile') || text.includes('Settings')) && 
                    !el.closest('[class*="Preferences"]') && 
                    !el.closest('[class*="nav-icon"]')) {
                    el.style.display = 'none';
                }
            });
        }
    }, 100);
})();
</script>
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
    <p style="opacity: 0.9;">📅 Member since January 2024</p>
</div>
""", unsafe_allow_html=True)

# Stats Overview
st.markdown("## 📊 Your Activity at a Glance")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{len(st.session_state.user_preferences.get('search_history', []))}</div>
        <div class="stat-label">Total Searches</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{len(st.session_state.user_preferences.get('liked_places', []))}</div>
        <div class="stat-label">Saved Places</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{len(st.session_state.user_preferences.get('dietary', []))}</div>
        <div class="stat-label">Dietary Preferences</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{len(st.session_state.user_preferences.get('cuisine_preferences', []))}</div>
        <div class="stat-label">Favorite Cuisines</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

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

st.divider()

# Current Preferences Summary
st.markdown("## ⚙️ Current Preferences")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🥗 Dietary Preferences")
    dietary = st.session_state.user_preferences.get('dietary', [])
    if dietary:
        for pref in dietary:
            st.markdown(f"✅ {pref}")
    else:
        st.info("No dietary restrictions set")
    
    st.markdown("### 💰 Price Range")
    price_range = st.session_state.user_preferences.get('price_range', [1, 4])
    if isinstance(price_range, tuple) or isinstance(price_range, list):
        if len(price_range) == 2 and isinstance(price_range[0], str):
            st.markdown(f"**{price_range[0]} to {price_range[1]}**")
        else:
            st.markdown(f"**{'$' * price_range[0]} to {'$' * price_range[1]}**")
    else:
        st.markdown("**$ to $$$$**")

with col2:
    st.markdown("### 🔊 Atmosphere")
    noise = st.session_state.user_preferences.get('noise_preference', 'Any')
    st.markdown(f"**{noise}**")
    
    st.markdown("### 📍 Default Location")
    location = st.session_state.user_preferences.get('location', 'San Jose, CA')
    st.markdown(f"**{location}**")

st.info("💡 **Tip:** Update your preferences in the sidebar on the main chat page!")

st.divider()

# Favorite Cuisines
st.markdown("## 🍜 Favorite Cuisines")
cuisines = st.session_state.user_preferences.get('cuisine_preferences', [])
if cuisines:
    cols = st.columns(4)
    for idx, cuisine in enumerate(cuisines):
        with cols[idx % 4]:
            st.markdown(f"🍽️ {cuisine}")
else:
    st.info("No cuisine preferences set yet. We'll learn as you explore!")

st.divider()

# Recent Activity
st.markdown("## 📅 Recent Activity")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔍 Recent Searches")
    recent_searches = st.session_state.user_preferences.get('search_history', [])[-5:]
    if recent_searches:
        for search in recent_searches:
            st.markdown(f"- {search.get('query', 'Unknown query')}")
    else:
        st.info("No recent searches")

with col2:
    st.markdown("### ❤️ Recently Saved")
    recent_saved = st.session_state.user_preferences.get('liked_places', [])[-5:]
    if recent_saved:
        for place in recent_saved:
            st.markdown(f"- {place}")
    else:
        st.info("No saved places yet")

st.divider()

# Account Actions
st.markdown("## ⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Update Profile", use_container_width=True, type="primary"):
        st.session_state.user_data['name'] = name
        st.session_state.user_data['email'] = email
        st.success("✅ Profile updated successfully!")

with col2:
    if st.button("📥 Export My Data", use_container_width=True):
        import json
        data = {
            'user_data': st.session_state.user_data,
            'preferences': st.session_state.user_preferences
        }
        st.download_button(
            "Download JSON",
            data=json.dumps(data, indent=2),
            file_name="spotlight_profile.json",
            mime="application/json"
        )

with col3:
    if st.button("🏠 Back to Chat", use_container_width=True):
        st.switch_page("app.py")

st.divider()

# Danger Zone
with st.expander("⚠️ Danger Zone"):
    st.warning("**Warning:** These actions cannot be undone!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear All Preferences", type="secondary"):
            if st.checkbox("I understand this will reset all my preferences"):
                st.session_state.user_preferences = {
                    'dietary': [],
                    'price_range': [1, 4],
                    'noise_preference': 'Any',
                    'cuisine_preferences': [],
                    'location': 'San Jose, CA',
                    'liked_places': [],
                    'search_history': []
                }
                st.warning("All preferences cleared!")
                st.rerun()
    
    with col2:
        if st.button("❌ Delete Account", type="secondary"):
            st.error("Account deletion is not available in demo mode")


