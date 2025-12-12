import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import json

# Page config
st.set_page_config(
    page_title="Spotlight AI - History",
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
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {
        'liked_places': ["Blue Bottle Coffee", "Cafe Frascati", "Philz Coffee"],
        'search_history': [
            {'query': 'coffee shops near me', 'timestamp': '2025-11-10 14:30:00', 'results': 5},
            {'query': 'italian restaurants', 'timestamp': '2025-11-09 19:15:00', 'results': 8},
            {'query': 'quiet study spots', 'timestamp': '2025-11-08 10:00:00', 'results': 3},
            {'query': 'brunch places downtown', 'timestamp': '2025-11-07 11:45:00', 'results': 6}
        ],
        'feedback_history': [
            {'place': 'Blue Bottle Coffee', 'feedback': 'liked', 'date': '2025-11-10'},
            {'place': 'The Grill', 'feedback': 'disliked', 'date': '2025-11-09'},
            {'place': 'Cafe Frascati', 'feedback': 'liked', 'date': '2025-11-08'}
        ]
    }

if 'saved_places' not in st.session_state:
    st.session_state.saved_places = [
        {
            'name': 'Blue Bottle Coffee',
            'rating': 4.5,
            'price': '$$',
            'category': 'Coffee & Tea',
            'saved_date': '2025-11-10',
            'visit_count': 3,
            'notes': 'Fast WiFi, has outlets!'
        },
        {
            'name': 'Cafe Frascati',
            'rating': 4.3,
            'price': '$$',
            'category': 'Coffee & Tea',
            'saved_date': '2025-11-08',
            'visit_count': 2,
            'notes': 'Love the outdoor seating.'
        },
        {
            'name': 'Philz Coffee',
            'rating': 4.6,
            'price': '$',
            'category': 'Coffee & Tea',
            'saved_date': '2025-11-05',
            'visit_count': 5,
            'notes': 'Best customized coffee blends!'
        }
    ]

# Page Header
st.title("History & Saved Places")

# Summary Stats
st.markdown("### Activity Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-box">
        <h2 style="color: #f44336; margin: 0;">""" + str(len(st.session_state.user_preferences.get('search_history', []))) + """</h2>
        <p style="color: #6c757d; margin: 5px 0 0 0;">Total Searches</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-box">
        <h2 style="color: #f44336; margin: 0;">""" + str(len(st.session_state.saved_places)) + """</h2>
        <p style="color: #6c757d; margin: 5px 0 0 0;">Saved Places</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    liked_count = len([f for f in st.session_state.user_preferences.get('feedback_history', []) if f['feedback'] == 'liked'])
    st.markdown("""
    <div class="stat-box">
        <h2 style="color: #f44336; margin: 0;">""" + str(liked_count) + """</h2>
        <p style="color: #6c757d; margin: 5px 0 0 0;">Places Liked</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_visits = sum([place['visit_count'] for place in st.session_state.saved_places])
    st.markdown("""
    <div class="stat-box">
        <h2 style="color: #f44336; margin: 0;">""" + str(total_visits) + """</h2>
        <p style="color: #6c757d; margin: 5px 0 0 0;">Total Visits</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Main Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Saved Places", "Search History", "Feedback History", "Recommendations"])

with tab1:
    st.markdown("### Your Saved Places")
    
    # Filter and sort options
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        sort_saved = st.selectbox("Sort by:", ["Most Recent", "Most Visited", "Highest Rated", "Name A-Z"])
    with col2:
        filter_category = st.multiselect("Filter by category:", ["Coffee & Tea", "Restaurants", "Bars", "Cafes"])
    
    
    st.markdown("---")
    
    # Display saved places
    if st.session_state.saved_places:
        for place in st.session_state.saved_places:
            st.markdown(f"""
            <div class="saved-card">
                <h3 style="margin-top: 0; color: #2c3e50;">{place['name']}</h3>
                <p style="margin: 5px 0;">
                    <strong>★ {place['rating']}</strong> • 
                    <strong>{place['price']}</strong> • 
                    <strong>{place['category']}</strong>
                </p>
                <p style="margin: 10px 0; color: #555;">
                    Saved on {place['saved_date']} • 
                    Visited {place['visit_count']} times
                </p>
                <p style="margin: 10px 0; font-style: italic; color: #666;">
                     "{place['notes']}"
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button(f"View on Map", key=f"map_{place['name']}"):
                    st.info(f"Opening map for {place['name']}")
            with col2:
                if st.button(f"Edit Notes", key=f"edit_{place['name']}"):
                    new_note = st.text_input(f"Update notes for {place['name']}", value=place['notes'], key=f"note_{place['name']}")
                    place['notes'] = new_note
            with col3:
                if st.button(f"Contact", key=f"contact_{place['name']}"):
                    st.info("Phone: (408) 555-0123")
            with col4:
                if st.button(f"Remove", key=f"remove_{place['name']}", type="secondary"):
                    st.session_state.saved_places.remove(place)
                    st.rerun()
    else:
        st.info("You haven't saved any places yet. Start exploring and save your favorites!")

with tab2:
    st.markdown("### Search History")
    st.caption("View your recent searches and results")
    
    # Time filter
    time_filter = st.selectbox("Show searches from:", ["Last 7 days", "Last 30 days", "Last 90 days", "All time"])
    
    st.markdown("---")
    
    # Display search history
    if st.session_state.user_preferences.get('search_history'):
        for idx, search in enumerate(st.session_state.user_preferences['search_history']):
            st.markdown(f"""
            <div class="history-item">
                <h4 style="margin: 0 0 5px 0; color: #2c3e50;">"{search['query']}"</h4>
                <p style="margin: 5px 0; color: #7f8c8d; font-size: 14px;">
                     {search['timestamp']} • 
                     {search['results']} results found
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                if st.button(f" Search Again", key=f"search_again_{idx}"):
                    st.info(f"Searching for: {search['query']}")
            with col2:
                if st.button(f" View Results", key=f"view_results_{idx}"):
                    st.info("Opening results...")
            with col3:
                if st.button(f"Delete", key=f"delete_search_{idx}"):
                    st.session_state.user_preferences['search_history'].remove(search)
                    st.rerun()
        
        st.markdown("---")
        if st.button("Clear All History", type="secondary"):
            if st.checkbox("Are you sure?"):
                st.session_state.user_preferences['search_history'] = []
                st.success("Search history cleared!")
                st.rerun()
    else:
        st.info("No search history yet. Start exploring to build your history!")

with tab3:
    st.markdown("### Feedback History")
    st.caption("See all the places you've liked or disliked")
    
    # Filter feedback
    feedback_filter = st.radio("Show:", ["All", "Liked Only", "Disliked Only"], horizontal=True)
    
    st.markdown("---")
    
    # Display feedback history
    if st.session_state.user_preferences.get('feedback_history'):
        for feedback in st.session_state.user_preferences['feedback_history']:
            badge_class = "badge-liked" if feedback['feedback'] == 'liked' else "badge-disliked"
            emoji = "" if feedback['feedback'] == 'liked' else " "
            
            st.markdown(f"""
            <div class="history-item">
                <span class="feedback-badge {badge_class}">{emoji} {feedback['feedback'].title()}</span>
                <h4 style="display: inline; margin-left: 10px; color: #2c3e50;">{feedback['place']}</h4>
                <p style="margin: 5px 0; color: #7f8c8d; font-size: 14px;"> {feedback['date']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(f" View Details", key=f"feedback_{feedback['place']}"):
                    st.info(f"Opening details for {feedback['place']}")
            with col2:
                if st.button(f"Delete", key=f"delete_feedback_{feedback['place']}"):
                    st.session_state.user_preferences['feedback_history'].remove(feedback)
                    st.rerun()
    else:
        st.info("No feedback history yet. Like or dislike places to build your profile!")

with tab4:
    st.markdown("### Personalized Recommendations")
    st.caption("Based on your saved places and feedback history")
    
    st.markdown("---")
    
    # Recommendation engine (mock)
    st.markdown("#### Places we think you'll like:")
    
    recommendations = [
        {
            'name': 'Chromatic Coffee',
            'rating': 4.7,
            'price': '$$',
            'reason': 'Similar to Blue Bottle Coffee which you saved',
            'match_score': 95
        },
        {
            'name': 'Red Rock Coffee',
            'rating': 4.4,
            'price': '$',
            'reason': 'Popular with people who like Philz Coffee',
            'match_score': 88
        },
        {
            'name': 'Academic Coffee',
            'rating': 4.6,
            'price': '$$',
            'reason': 'Quiet atmosphere - matches your preferences',
            'match_score': 92
        }
    ]
    
    for rec in recommendations:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div class="saved-card">
                <h4 style="margin-top: 0;">{rec['name']}</h4>
                <p style="margin: 5px 0;">★ {rec['rating']} • {rec['price']}</p>
                <p style="margin: 10px 0; color: #667eea; font-weight: bold;">
                     {rec['match_score']}% Match
                </p>
                <p style="margin: 5px 0; font-style: italic; color: #666;">
                     {rec['reason']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Explore", key=f"explore_{rec['name']}"):
                st.info(f"Opening {rec['name']}")
            if st.button("Save", key=f"save_rec_{rec['name']}"):
                st.success(f"Saved {rec['name']}!")

