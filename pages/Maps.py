import streamlit as st
import folium
from streamlit_folium import st_folium

# Chat interface
st.title("🔦 Spotlight AI")
prompt = st.chat_input("Find me a quiet coffee shop...")

# Display map
m = folium.Map(location=[37.3382, -121.8863])  # San Jose
st_folium(m, width=700, height=500)

# Sidebar for preferences
with st.sidebar:
    st.header("Your Preferences")
    budget = st.slider("Price Range", 1, 4)
    distance = st.slider("Distance (miles)", 1, 10)