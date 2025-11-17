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

# Custom CSS
st.markdown("""
<style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f5f5f5;
    }
    [data-testid="stSidebar"] > div:first-child {
        background-color: #f0f2f6;
    }
    /* Make sidebar headers bigger */
    [data-testid="stSidebar"] h2 {
        font-size: 1.5rem !important;
        font-weight: bold;
    }

 .stButton > button {
        background: #f44336;      /* main color */
        color: white;             /* text */
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        background: #bc342a;
    }

    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .place-card {
        border: 1px solid #ddd;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .place-header {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 8px;
        color: #2c3e50;
    }
    .place-rating {
        color: #f39c12;
        font-size: 14px;
        margin-bottom: 10px;
    }
    .citation {
        font-size: 13px;
        color: #555;
        font-style: italic;
        margin-top: 12px;
        padding: 10px;
        background-color: rgba(255,255,255,0.7);
        border-left: 4px solid #667eea;
        border-radius: 4px;
    }
    .source-link {
        color: #667eea;
        text-decoration: none;
        font-size: 12px;
    }
</style>
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
    if st.button("Search & Map", use_container_width=True):
        st.switch_page("pages/Maps.py")
    if st.button("Profile", use_container_width=True):
        st.switch_page("pages/Profile.py")
    if st.button("History", use_container_width=True):
        st.switch_page("pages/History.py")
    if st.button("Settings", use_container_width=True):
        st.switch_page("pages/Settings.py")
        st.divider()

    st.divider()

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
    

    
    
    
    
   
   # st.divider()
    
 

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
