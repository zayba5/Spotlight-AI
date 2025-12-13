import streamlit as st
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Spotlight AI - Search & Map",
    page_icon="🗺️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .result-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .result-header {
        font-size: 22px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 8px;
    }
    .result-meta {
        color: #7f8c8d;
        font-size: 14px;
        margin-bottom: 12px;
    }
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    .badge-open {
        background: #d4edda;
        color: #155724;
    }
    .badge-price {
        background: #fff3cd;
        color: #856404;
    }
    .badge-distance {
        background: #d1ecf1;
        color: #0c5460;
    }
    .filter-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'search_results' not in st.session_state:
    # Mock search results
    st.session_state.search_results = [
        {
            "name": "Blue Bottle Coffee",
            "rating": 4.5,
            "reviews": 312,
            "price": "$$",
            "category": "Coffee & Tea",
            "distance": 0.8,
            "address": "123 Main St, San Jose, CA",
            "open_now": True,
            "lat": 37.3352,
            "lng": -121.8811,
            "description": "Minimalist cafe with excellent espresso and plenty of workspace.",
            "hours": "7:00 AM - 8:00 PM"
        },
        {
            "name": "Cafe Frascati",
            "rating": 4.3,
            "reviews": 428,
            "price": "$$",
            "category": "Coffee & Tea",
            "distance": 1.2,
            "address": "456 Oak Ave, San Jose, CA",
            "open_now": True,
            "lat": 37.3318,
            "lng": -121.8906,
            "description": "European-style cafe with outdoor seating and amazing pastries.",
            "hours": "6:30 AM - 9:00 PM"
        },
        {
            "name": "Philz Coffee",
            "rating": 4.6,
            "reviews": 892,
            "price": "$",
            "category": "Coffee & Tea",
            "distance": 1.5,
            "address": "789 Park St, San Jose, CA",
            "open_now": True,
            "lat": 37.3290,
            "lng": -121.8850,
            "description": "Local favorite known for customized coffee blends.",
            "hours": "6:00 AM - 8:00 PM"
        },
        {
            "name": "Roy's Station Coffee",
            "rating": 4.7,
            "reviews": 245,
            "price": "$$",
            "category": "Coffee & Tea",
            "distance": 2.1,
            "address": "321 First St, San Jose, CA",
            "open_now": False,
            "lat": 37.3400,
            "lng": -121.8900,
            "description": "Artisanal roaster with a cozy neighborhood vibe.",
            "hours": "Closed • Opens at 7:00 AM tomorrow"
        }
    ]

# Sidebar Filters
with st.sidebar:
    st.markdown("###  Filters") 

    distance_radius = st.slider("📍 Distance (miles)", 0.5, 25.0, 5.0, 0.5)
    
    # Price Range
    price_filter = st.multiselect(
        "Price Range",
        ["$", "$$", "$$$", "$$$$"],
        default=["$", "$$"]
    )
    
    # Rating
    min_rating = st.slider("Minimum Rating", 1.0, 5.0, 4.0, 0.5)
    
    # Categories
    categories = st.multiselect(
        "Categories",
        ["Coffee & Tea", "Restaurants", "Cafes", "Bars", "Fast Food", "Desserts"],
        default=["Coffee & Tea"]
    )
    
    # Open Now
    open_now = st.checkbox("Open Now", value=True)
    
    # Sort By
    sort_by = st.selectbox(
        "Sort By",
        ["Distance", "Rating", "Reviews", "Price (Low to High)", "Price (High to Low)"]
    )
    
    st.divider()
    
    if st.button("Reset Filters", use_container_width=True):
        st.rerun()
    
    if st.button("Apply Filters", use_container_width=True, type="primary"):
        st.success("Filters applied!")

# Main Content
st.title("Search Results & Map View")

# Results summary
# Apply all filters
filtered_results = st.session_state.search_results.copy()

# Filter by price
if price_filter:
    filtered_results = [r for r in filtered_results if r['price'] in price_filter]

# Filter by rating
filtered_results = [r for r in filtered_results if r['rating'] >= min_rating]

# Filter by categories
if categories:
    filtered_results = [r for r in filtered_results if r['category'] in categories]

# Filter by distance
filtered_results = [r for r in filtered_results if r['distance'] <= distance_radius]

# Filter by open now
if open_now:
    filtered_results = [r for r in filtered_results if r['open_now']]

# Apply sorting
if sort_by == "Distance":
    filtered_results = sorted(filtered_results, key=lambda x: x['distance'])
elif sort_by == "Rating":
    filtered_results = sorted(filtered_results, key=lambda x: x['rating'], reverse=True)
elif sort_by == "Reviews":
    filtered_results = sorted(filtered_results, key=lambda x: x['reviews'], reverse=True)
elif sort_by == "Price (Low to High)":
    price_order = {"$": 1, "$$": 2, "$$$": 3, "$$$$": 4}
    filtered_results = sorted(filtered_results, key=lambda x: price_order.get(x['price'], 5))
elif sort_by == "Price (High to Low)":
    price_order = {"$": 1, "$$": 2, "$$$": 3, "$$$$": 4}
    filtered_results = sorted(filtered_results, key=lambda x: price_order.get(x['price'], 5), reverse=True)

st.markdown(f"### Found {len(filtered_results)} places within {distance_radius} miles")

# View toggle
view_mode = st.radio("View Mode:", ["List View", "Map View"], horizontal=True)

# Helper function to prepare map data
def prepare_map_data(results):
    """Convert results to DataFrame format for st.map()"""
    if not results:
        return pd.DataFrame()
    
    map_data = []
    for result in results:
        map_data.append({
            "lat": result["lat"],
            "lon": result["lng"],  # st.map uses 'lon' not 'lng'
            "name": result["name"],
            "rating": result["rating"],
            "reviews": result["reviews"],
            "price": result["price"],
            "distance": result["distance"]
        })
    
    return pd.DataFrame(map_data)

if view_mode == "List View":
    # List view only
    for result in filtered_results:
        with st.container():
            st.markdown(f"""
            <div class="result-card">
                <div class="result-header">{result['name']}</div>
                <div class="result-meta">
                    ★ {result['rating']} ({result['reviews']} reviews) • 
                    {result['price']} • 
                    {result['category']}
                </div>
                <div>
                    <span class="badge {'badge-open' if result['open_now'] else 'badge-closed'}">{result['hours']}</span>
                    <span class="badge badge-distance"> {result['distance']} mi</span>
                    <span class="badge badge-price">{result['price']}</span>
                </div>
                <p style="margin-top: 12px; color: #555;">{result['description']}</p>
                <p style="font-size: 14px; color: #7f8c8d;"> {result['address']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("Directions", key=f"dir_{result['name']}"):
                    st.info(f"Opening directions to {result['name']}")
            with col2:
                if st.button("Details", key=f"details_{result['name']}"):
                    with st.expander(f"Details for {result['name']}", expanded=True):
                        st.markdown(f"** Rating:** {result['rating']}/5.0")
                        st.markdown(f"** Reviews:** {result['reviews']}")
                        st.markdown(f"** Price:** {result['price']}")
                        st.markdown(f"** Address:** {result['address']}")
                        st.markdown(f"** Hours:** {result['hours']}")
                        st.markdown(f"** Distance:** {result['distance']} miles")
                        st.markdown("---")
                        st.markdown("**Recent Reviews:**")
                        st.markdown("> Great coffee and atmosphere! Perfect for working.")
                        st.markdown("> Friendly staff and quick service.")
            with col3:
                if st.button("Save", key=f"save_{result['name']}"):
                    st.success(f"Saved {result['name']}!")
            with col4:
                if st.button("Call", key=f"call_{result['name']}"):
                    st.info("Phone: (408) 555-0123")

elif view_mode == "Map View":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Results")
        for result in filtered_results[:3]:  # Show first 3 in split view
            st.markdown(f"""
            <div class="result-card">
                <div class="result-header">{result['name']}</div>
                <div class="result-meta">★ {result['rating']} • {result['price']} • {result['distance']} mi</div>
                <span class="badge {'badge-open' if result['open_now'] else ''}">{result['hours']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Initialize expander state for this place
            expander_key = f"expander_{result['name']}"
            if expander_key not in st.session_state:
                st.session_state[expander_key] = False
            
            # Toggle expander state when button is clicked
            if st.button(f"View Details", key=f"split_view_{result['name']}"):
                st.session_state[expander_key] = not st.session_state[expander_key]
            
            # Show expander based on state
            if st.session_state[expander_key]:
                with st.expander(f"Details for {result['name']}", expanded=True):
                    st.markdown(f"**Address:** {result.get('address', 'N/A')}")
                    st.markdown("---")
                    st.markdown(f"**Details:**")
                    st.markdown(f"{result.get('description', 'No description available.')}")
                    st.markdown("---")
                    st.markdown(f"**Phone Number:** {result.get('phone', 'N/A')}")
    
    with col2:
        st.markdown("### Map")
        map_df = prepare_map_data(filtered_results)
        
        if not map_df.empty:
            st.map(map_df, zoom=13)
        else:
            st.info("No places to display on the map.")


