import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# Page config
st.set_page_config(
    page_title="Spotlight AI - History",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
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
    
   
