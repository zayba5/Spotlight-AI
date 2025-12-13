BACKEND_URL = "http://localhost:8000/chat"

import streamlit as st
import json
import os
from datetime import datetime
import requests
from geopy.geocoders import Nominatim

def render_place_card(place):
    """
    Render a single interactive place card in Streamlit
    """
    st.markdown(f"""
        <div class="place-card">
            <div class="place-header">{place.get('name', place.get('title', 'Unknown'))}</div>
            <div class="place-rating">⭐ {place.get('rating', '?')} ({place.get('reviews', place.get('review_count', '?'))} reviews)</div>
            <p>{place.get('description', '')}</p>
            <div class="citation">{place.get('citation', place.get('random_review', ''))}</div>
        </div>
    """, unsafe_allow_html=True)

    # Add two buttons side by side
    col1, col2 = st.columns([1, 1])
    with col1:
        place_name = place.get('name', place.get('title', 'Unknown'))

        if st.button(
            f"❤️ Save {place_name}",
            key=f"save_{place_name}"
        ):
            already_saved = any(
                p["name"] == place_name
                for p in st.session_state.saved_places
            )

            if not already_saved:
                st.session_state.saved_places.append({
                    "name": place_name,
                    "rating": place.get("rating", "?"),
                    "price": place.get("price", "$$"),
                    "category": place.get("category", "Restaurant"),
                    "saved_date": datetime.now().strftime("%Y-%m-%d"),
                    "visit_count": 0,          # REQUIRED by History.py
                    "notes": place.get("description", ""),
                })

                st.success(f"Saved {place_name}!")

                # Optional: jump straight to History page
                st.switch_page("pages/History.py")

            else:
                st.info(f"{place_name} is already saved.")

    with col2:
        if st.button(f"🗺️ View on Map", key=f"map_{place.get('name', place.get('title', 'Unknown'))}"):
            st.info(f"Opening map for {place.get('name', place.get('title', 'Unknown'))}…")


# Initialize saved places list
if "saved_places" not in st.session_state:
    st.session_state.saved_places = []


# Page config
st.set_page_config(
    page_title="Spotlight AI - Chat",
    #page_icon="🔦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Top Navigation Bar (HTML + CSS)
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
            
    /* Buttons */
    .stButton > button {
        background: #f44336;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.45rem 0.75rem;
        font-size: 0.9rem;
        font-weight: 600;
        transition: all 0.15s ease;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.08);
    }
    .stButton > button:hover {
        background: #a51818;
        transform: translateY(-1px);
        box-shadow: 0px 3px 6px rgba(0,0,0,0.12);
    }

    /* Chat messages */
    .stChatMessage {
        padding: 1rem;
        border-radius: 12px;
        background: #fff;
        border: 1px solid #eee;
        margin-bottom: 0.75rem;
        box-shadow: 0px 1px 3px rgba(0,0,0,0.06);
    }

    /* Place cards */
    .place-card {
        border: 1px solid #eee;
        border-radius: 12px;
        padding: 18px;
        margin: 12px 0;
        background: #fff;
        box-shadow: 0 3px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .place-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.12);
    }

    .place-header {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 6px;
        color: #f44336;
    }

    .place-rating {
        color: #f39c12;
        font-size: 14px;
        margin-bottom: 8px;
        font-weight: 500;
    }

    .citation {
        font-size: 13px;
        color: #555;
        font-style: italic;
        margin-top: 10px;
        padding: 8px;
        background-color: #f8f8f8;
        border-left: 4px solid #f44336;
        border-radius: 4px;
    }

    .source-link {
        color: #f44336;
        text-decoration: none;
        font-size: 12px;
        font-weight: 500;
    }
    .source-link:hover {
        text-decoration: underline;
    }


</style>
""", unsafe_allow_html=True)

# Determine current page for highlighting
current_file = os.path.basename(__file__)
if current_file == "Homepage.py":
    current_page_name = "homepage"
else:
    current_page_name = current_file.replace(".py", "").lower()

# Check query params for page navigation - MUST BE FIRST
query_params = st.query_params
if 'nav' in query_params:
    nav_page = query_params['nav']
    current_file_name = os.path.basename(__file__)
    
    if nav_page == 'homepage' and current_file_name != "Homepage.py":
        st.switch_page("Homepage.py")
    elif nav_page == 'history' and current_file_name != "History.py":
        st.switch_page("pages/History.py")
    elif nav_page == 'maps' and current_file_name != "Maps.py":
        st.switch_page("pages/Maps.py")
    elif nav_page == 'profile' and current_file_name != "Profile.py":
        st.switch_page("pages/Profile.py")
    elif nav_page == 'settings' and current_file_name != "Settings.py":
        st.switch_page("pages/Settings.py")

# Top Navigation Bar with Icons - Using anchor tags for direct navigation
nav_html = f"""
<div class="custom-top-nav">
    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/No_image_available_600_x_450.svg">
    <div class="search-wrapper">
        <input type="text" placeholder="Search Spotlight AI...">
    </div>
    <div class="nav-icons-top">
        <a href="/"  target="_self" class="nav-icon-top {'active' if current_page_name == 'homepage' else ''}" 
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


# Add a search bar at the top
st.markdown("""
""", unsafe_allow_html=True)


# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = True  # Set to True for demo
if 'user_data' not in st.session_state:
    st.session_state.user_data = {'email': 'demo@spotlight.ai', 'name': 'Demo User'}
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {
        'dietary': [],
        'price_range': [1, 4],
        'noise_preference': 'Any',
        'cuisine_preferences': [],
        'location': 'San Jose, CA',  # default location
        'liked_places': [],
        'search_history': [],
        'distance_miles': 5,
        'open_now': True,
    }
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

# Sidebar - Preferences and Filters
with st.sidebar:

    st.header("**Preferences:**")
    
    # Location
    st.subheader("📍 Location")
    user_location = st.text_input("Current Location", value=st.session_state.user_preferences.get('location', 'San Jose, CA'))
    distance_radius = st.slider(
        "Search Radius (miles)",
        1,
        25,
        int(st.session_state.user_preferences.get('distance_miles', 5)),
    )
    st.session_state.user_preferences['location'] = user_location
    st.session_state.user_preferences['distance_miles'] = distance_radius
    
    # Save preferences
    if st.button("Save Preferences"):
        st.success("Preferences saved!")


# Main content area
st.title("🔦 Spotlight AI")
st.caption("Your personal local search assistant")

# Suggested prompts for new users
if len(st.session_state.messages) == 0:
    st.markdown("### 💬 Try asking me:")
    prompt_cols = st.columns(2)
    with prompt_cols[0]:
        if st.button("🍕 Best pizza near me"):
            user_query = "Best pizza near me"
            st.session_state.messages.append({"role": "user", "content": user_query})
            st.rerun()
        if st.button("☕️ Quiet coffee shops with WiFi"):
            user_query = "Quiet coffee shops with WiFi"
            st.session_state.messages.append({"role": "user", "content": user_query})
            st.rerun()
    with prompt_cols[1]:
        if st.button("🍜 Late night food options"):
            user_query = "Late night food options"
            st.session_state.messages.append({"role": "user", "content": user_query})
            st.rerun()
        if st.button("🥗 Healthy lunch under $15"):
            user_query = "Healthy lunch under $15"
            st.session_state.messages.append({"role": "user", "content": user_query})
            st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display place cards if it's an assistant message with recommendations
        if message["role"] == "assistant" and "places" in message:
            for place in message["places"]:
                render_place_card(place)


# Chat input
if prompt := st.chat_input("Ask me about local places..."):
    # Add to search history
    st.session_state.user_preferences['search_history'].append({
        'query': prompt,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Geocode user location (once)
            geolocator = Nominatim(user_agent="spotlight_ai")
            user_location_str = st.session_state.user_preferences.get("location", None)
            latitude, longitude = None, None
            if user_location_str:
                try:
                    location = geolocator.geocode(user_location_str)
                    if location:
                        latitude = location.latitude
                        longitude = location.longitude
                except Exception as e:
                    st.warning(f"Geocoding failed: {e}")

            # Active filters to send to the backend /chat endpoint
            # For now we only use distance; other UI filters are not exposed.
            filters = {
                "distance_miles": st.session_state.user_preferences.get("distance_miles", 5),
            }

            # Prepare request payload
            payload = {
                "user_id": st.session_state.user_data["email"],
                "query": prompt,
                "location_hint": user_location_str,
                "latitude": latitude,
                "longitude": longitude,
                "update_preferences": None,
                "conversation_id": None,
                "filters": filters,
            }


            try:
                response = requests.post(BACKEND_URL, json=payload, timeout=60)

                if response.status_code != 200:
                    st.error(f"Backend error: {response.text}")
                    assistant_answer = ""
                    citations = []
                else:
                    data = response.json()
                    assistant_answer = data.get("answer", "")
                    citations = data.get("citations", [])

                # Extract citations from backend response
                places = []  # frontend expects "places"

                if "citations" in data and isinstance(data["citations"], list):
                    def clean_text(text):
                        if not text:
                            return ""
                        return text.replace("***", "").strip()

                for c in data["citations"]:
                        places.append({
                            "name": clean_text(c.get("title", "Unknown")),
                            "rating": c.get("rating", "?"),
                            "reviews": c.get("review_count", "?"),
                            "description": clean_text(c.get("description", "")),
                            "citation": clean_text(c.get("random_review", ""))
                        })

                # Add assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_answer if len(places) == 0 else "",
                    "places": places  # map citations to places so frontend renders cards
                })


                st.rerun()

            except Exception as e:
                st.error(f"Unable to contact backend: {e}")


# Footer
st.divider()
#st.caption("🔦 Spotlight AI • Powered by RAG + Yelp + Google Places • Built by Howard, Zayba, and Tiana")
