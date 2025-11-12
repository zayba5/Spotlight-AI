import streamlit as st
import folium
from streamlit_folium import st_folium
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Spotlight AI",
    page_icon="🔦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better chat appearance
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .place-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .place-header {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .place-rating {
        color: #ffa500;
        font-size: 14px;
    }
    .citation {
        font-size: 12px;
        color: #666;
        font-style: italic;
        margin-top: 10px;
        padding: 8px;
        background-color: #f0f0f0;
        border-left: 3px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {
        'dietary': [],
        'price_range': [1, 4],
        'noise_preference': 'Any',
        'liked_places': []
    }
if 'show_map' not in st.session_state:
    st.session_state.show_map = False

# Sidebar - User Preferences & Memory
with st.sidebar:
    st.header("🎯 Your Preferences")
    
    # Location
    st.subheader("📍 Location")
    user_location = st.text_input("Current Location", "San Jose, CA")
    distance_radius = st.slider("Search Radius (miles)", 1, 25, 5)
    
    # Preferences
    st.subheader("⚙️ Filters")
    price_range = st.select_slider(
        "Price Range",
        options=["$", "$$", "$$$", "$$$$"],
        value=("$", "$$$$")
    )
    
    dietary_prefs = st.multiselect(
        "Dietary Preferences",
        ["Vegetarian", "Vegan", "Gluten-Free", "Halal", "Kosher"]
    )
    
    noise_level = st.radio(
        "Noise Preference",
        ["Any", "Quiet", "Moderate", "Lively"]
    )
    
    open_now = st.checkbox("Open Now", value=True)
    
    # Save preferences
    if st.button("Save Preferences"):
        st.session_state.user_preferences.update({
            'dietary': dietary_prefs,
            'price_range': price_range,
            'noise_preference': noise_level
        })
        st.success("Preferences saved!")
    
    st.divider()
    
    # Memory Display
    st.subheader("🧠 What I Remember")
    if st.session_state.user_preferences['liked_places']:
        st.write("**Your favorite places:**")
        for place in st.session_state.user_preferences['liked_places'][-3:]:
            st.write(f"• {place}")
    else:
        st.info("I'll learn your preferences as we chat!")
    
    if dietary_prefs:
        st.write(f"**Dietary:** {', '.join(dietary_prefs)}")
    
    if st.button("Clear Memory"):
        st.session_state.user_preferences['liked_places'] = []
        st.rerun()

# Main content area
st.title("🔦 Spotlight AI")
st.caption("Your personal local search assistant")

# Layout: Chat and Map side by side
col1, col2 = st.columns([3, 2] if st.session_state.show_map else [1, 0.001])

with col1:
    # Suggested prompts for new users
    if len(st.session_state.messages) == 0:
        st.markdown("### 💬 Try asking me:")
        prompt_cols = st.columns(2)
        with prompt_cols[0]:
            if st.button("🍕 Best pizza near me"):
                user_query = "Best pizza near me"
                st.session_state.messages.append({"role": "user", "content": user_query})
                st.rerun()
            if st.button("☕ Quiet coffee shops with WiFi"):
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
                        if st.button(f"📍 Directions", key=f"dir_{place['name']}_{len(st.session_state.messages)}"):
                            st.info(f"Opening directions to {place['name']}...")
                    with btn_cols[1]:
                        if st.button(f"❤️ Save", key=f"save_{place['name']}_{len(st.session_state.messages)}"):
                            if place['name'] not in st.session_state.user_preferences['liked_places']:
                                st.session_state.user_preferences['liked_places'].append(place['name'])
                                st.success(f"Saved {place['name']}!")
                    with btn_cols[2]:
                        if st.button(f"ℹ️ More Info", key=f"info_{place['name']}_{len(st.session_state.messages)}"):
                            st.info(f"Opening Yelp page for {place['name']}...")
                
                # Add assistant message to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "places": mock_places
                })
                
                # Show map button
                if st.button("🗺️ View All on Map"):
                    st.session_state.show_map = True
                    st.rerun()

# Map view (right column)
with col2:
    if st.session_state.show_map and len(st.session_state.messages) > 0:
        st.subheader("📍 Map View")
        
        # Create map centered on San Jose
        m = folium.Map(
            location=[37.3382, -121.8863],
            zoom_start=13,
            tiles="OpenStreetMap"
        )
        
        # Add markers for recommended places
        # TODO: Get coordinates from your actual data
        example_locations = [
            {"name": "Blue Bottle Coffee", "lat": 37.3352, "lng": -121.8811, "rating": 4.5},
            {"name": "Cafe Frascati", "lat": 37.3318, "lng": -121.8906, "rating": 4.3}
        ]
        
        for loc in example_locations:
            folium.Marker(
                location=[loc['lat'], loc['lng']],
                popup=f"<b>{loc['name']}</b><br>⭐ {loc['rating']}",
                tooltip=loc['name'],
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
        
        # Display map
        st_folium(m, width=700, height=600)
        
        if st.button("✖️ Hide Map"):
            st.session_state.show_map = False
            st.rerun()

# Footer
st.divider()
#st.caption("Built with ❤️ by Howard, Zayba, and Tiana | Powered by RAG + Yelp + Google Places")