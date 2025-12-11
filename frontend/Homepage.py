import streamlit as st
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Spotlight AI - Chat",
    #page_icon="🔦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Top Navigation Bar (HTML + CSS)
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

    .custom-top-nav input {
        flex-grow: 1;
        max-width: 500px;
        height: 36px;
        border: none;
        border-radius: 18px;
        padding: 0 16px;
        background: #fff;
        outline: none;
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

<div class="custom-top-nav">
    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/No_image_available_600_x_450.svg">
    <input type="text" placeholder="Search Spotlight AI...">
</div>
""", unsafe_allow_html=True)


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
        'location': 'San Jose, CA', #default location
        'liked_places': [],
        'search_history': []
    }

# Sidebar - Preferences and Filters
with st.sidebar:
    # Remove all the buttons here — no navigation buttons at all

    st.header("**Preferences:**")
    
    # Location
    st.subheader("📍 Location")
    user_location = st.text_input("Current Location", value=st.session_state.user_preferences.get('location', 'San Jose, CA'))
    distance_radius = st.slider("Search Radius (miles)", 1, 25, 5)
    st.session_state.user_preferences['location'] = user_location
    
    # Preferences
    st.subheader("⚙️ Filters")
    price_range = st.select_slider(
        "Price Range",
        options=["$", "$$", "$$$", "$$$$"],
        value=("$", "$$$$")
    )
    st.session_state.user_preferences['price_range'] = price_range
    
    dietary_prefs = st.multiselect(
        "Dietary Preferences",
        ["Vegetarian", "Vegan", "Gluten-Free", "Halal", "Kosher"],
        default=st.session_state.user_preferences.get('dietary', [])
    )
    st.session_state.user_preferences['dietary'] = dietary_prefs
    
    noise_level = st.radio(
        "Noise Preference",
        ["Any", "Quiet", "Moderate", "Lively"],
        index=["Any", "Quiet", "Moderate", "Lively"].index(st.session_state.user_preferences.get('noise_preference', 'Any'))
    )
    st.session_state.user_preferences['noise_preference'] = noise_level
    
    open_now = st.checkbox("Open Now", value=True)
    
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
                st.markdown(f"""
                <div class="place-card">
                    <div class="place-header">{place['name']}</div>
                    <div class="place-rating">⭐ {place['rating']} ({place['reviews']} reviews) • {place['price']}</div>
                    <p>{place['description']}</p>
                    <div class="citation">💬 "{place['citation']}" - Yelp Review</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                btn_cols = st.columns(3)
                with btn_cols[0]:
                    if st.button(f"📍 Directions", key=f"dir_{place['name']}"):
                        st.info(f"Opening directions to {place['name']}...")
                with btn_cols[1]:
                    if st.button(f"❤️ Save", key=f"save_{place['name']}"):
                        if place['name'] not in st.session_state.user_preferences['liked_places']:
                            st.session_state.user_preferences['liked_places'].append(place['name'])
                            st.success(f"Saved {place['name']}!")
                with btn_cols[2]:
                    if st.button(f"ℹ️ More Info", key=f"info_{place['name']}"):
                        st.info(f"Opening Yelp page for {place['name']}...")

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
    
    # Generate AI response (mock for now - you'll replace with your RAG pipeline)
    with st.chat_message("assistant"):
        with st.spinner("Searching local places..."):
            # TODO: Replace with your actual RAG pipeline
            # response = your_rag_pipeline(prompt, st.session_state.user_preferences)
            
            # Mock response for demonstration
            response_text = f"Based on your query '{prompt}' and preferences, here are my top recommendations:"
            st.markdown(response_text)
            
            # Mock place data (replace with actual Yelp/Google API data)
            mock_places = [
                {
                    "name": "Blue Bottle Coffee",
                    "rating": 4.5,
                    "reviews": 312,
                    "price": "$$",
                    "description": "Minimalist cafe with excellent espresso, plenty of outlets, and a quiet atmosphere perfect for working.",
                    "citation": "Great place to work! Quiet, fast WiFi, and the coffee is amazing.",
                    "lat": 37.3352,
                    "lng": -121.8811
                },
                {
                    "name": "Cafe Frascati",
                    "rating": 4.3,
                    "reviews": 428,
                    "price": "$$",
                    "description": "Cozy European-style cafe with outdoor seating and reliable WiFi. Known for their pastries.",
                    "citation": "Love this spot for morning work sessions. Never too crowded and staff is friendly.",
                    "lat": 37.3318,
                    "lng": -121.8906
                }
            ]
            
            # Display places
            for place in mock_places:
                st.markdown(f"""
                <div class="place-card">
                    <div class="place-header">{place['name']}</div>
                    <div class="place-rating">⭐ {place['rating']} ({place['reviews']} reviews) • {place['price']}</div>
                    <p>{place['description']}</p>
                    <div class="citation">💬 "{place['citation']}" - Yelp Review</div>
                </div>
                """, unsafe_allow_html=True)
                
                btn_cols = st.columns(3)
                with btn_cols[0]:
                    if st.button(f"📍 Directions", key=f"dir_{place['name']}_new"):
                        st.info(f"Opening directions to {place['name']}...")
                with btn_cols[1]:
                    if st.button(f"❤️ Save", key=f"save_{place['name']}_new"):
                        if place['name'] not in st.session_state.user_preferences['liked_places']:
                            st.session_state.user_preferences['liked_places'].append(place['name'])
                            st.success(f"Saved {place['name']}!")
                with btn_cols[2]:
                    if st.button(f"ℹ️ More Info", key=f"info_{place['name']}_new"):
                        st.info(f"Opening Yelp page for {place['name']}...")
            
            # Add assistant message to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "places": mock_places
            })

# Footer
st.divider()
#st.caption("🔦 Spotlight AI • Powered by RAG + Yelp + Google Places • Built by Howard, Zayba, and Tiana")
