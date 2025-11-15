import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Spotlight AI - Profile",
    page_icon="👤",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .profile-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        color: #667eea;
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
    st.session_state.user_data = {'email': 'demo@spotlight.ai', 'name': 'Demo User'}
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
st.markdown("## 👤 Account Information")

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

# Footer
st.divider()
st.caption("🔒 Your data is private and secure. We never share your information with third parties.")