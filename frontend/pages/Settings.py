import streamlit as st

# Page config
st.set_page_config(
    page_title="Spotlight AI - About & Help",
    page_icon="ℹ️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .hero-section {
        background: linear-gradient(135deg, #f44336 0%, #c62828 100%);
        padding: 3rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #f44336;
    }
    .example-query {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #f44336;
        margin: 10px 0;
        font-family: monospace;
    }
    .example-section {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    .faq-item {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .team-card {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .citation-box {
        background: #e7f3ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0066cc;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 style="margin: 0; font-size: 3rem;">🔦 Spotlight AI</h1>
    <p style="font-size: 1.3rem; margin: 1rem 0;">Real-Time, Personalized Local Search</p>
    <p style="font-size: 1.1rem; opacity: 0.9;">Your AI-powered assistant for discovering the best local places</p>
</div>
""", unsafe_allow_html=True)

# Main Tabs
tab1, tab2, tab3 = st.tabs(["🎯 About", "💡 Examples", "📚 Citations Page"])

with tab1:
    st.markdown("## 🎯 About Spotlight AI")
    
    st.markdown("""
    Spotlight AI is a revolutionary chat-based recommendation system that transforms how you discover local businesses. 
    Unlike traditional review platforms that overwhelm you with information, we provide **personalized, conversational, 
    and actionable recommendations** powered by AI.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>AI-Powered Intelligence</h3>
            <p>Our advanced RAG (Retrieval-Augmented Generation) pipeline analyzes thousands of reviews 
            to give you concise, relevant answers to your questions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>Personalized Results</h3>
            <p>Spotlight AI learns your preferences over time - dietary restrictions, budget, atmosphere - 
            to provide increasingly tailored recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>Real-Time Data</h3>
            <p>We integrate live data from Yelp and Google Places to ensure you always get current 
            information about hours, menus, and reviews.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>Natural Conversation</h3>
            <p>Just ask questions in plain English. No need to navigate complex filters or 
            sort through endless reviews.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>Location-Aware</h3>
            <p>Automatic location detection ensures recommendations are always relevant to where you are 
            or where you're going.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>Transparent Citations</h3>
            <p>Every recommendation includes links to source reviews, so you can verify 
            and explore further with confidence.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### Technology Stack")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **Frontend:**
        - Streamlit
        - Python
        - Interactive Maps
        """)
    with col2:
        st.markdown("""
        **Backend:**
        - FastAPI
        - RAG Pipeline (LangChain)
        - ChromaDB (Vector Store)
        """)
    with col3:
        st.markdown("""
        **Data Sources:**
        - Yelp API
        - Google Places API
        - OpenStreetMap
        """)

with tab2:
    st.markdown("## 💡 Example Queries")
    st.caption("Try these sample queries to see what Spotlight AI can do:")
    
    # Food & Dining Section
    st.markdown("""
    <div class="example-section">
        <h3 style="margin-top: 0; color: #f44336;"> Food & Dining</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        food_examples = [
            "Find me vegetarian restaurants under $20 near downtown",
            "What are the best brunch spots with outdoor seating?",
            "Show me highly-rated sushi restaurants within 5 miles"
        ]
        
        for example in food_examples:
            st.markdown(f'<div class="example-query">"{example}"</div>', unsafe_allow_html=True)
    
    with col2:
        food_examples_2 = [
            "Late night food options that are open now",
            "Italian restaurants good for a date night"
        ]
        
        for example in food_examples_2:
            st.markdown(f'<div class="example-query">"{example}"</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Work & Study Section
    st.markdown("""
    <div class="example-section">
        <h3 style="margin-top: 0; color: #f44336;">Work & Study</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        work_examples = [
            "Quiet coffee shops with WiFi for working",
            "Study spots open late with good coffee"
        ]
        
        for example in work_examples:
            st.markdown(f'<div class="example-query"> "{example}"</div>', unsafe_allow_html=True)
    
    with col2:
        work_examples_2 = [
            "Cafes with power outlets and comfortable seating"
        ]
        
        for example in work_examples_2:
            st.markdown(f'<div class="example-query"> "{example}"</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Entertainment & Nightlife Section
    st.markdown("""
    <div class="example-section">
        <h3 style="margin-top: 0; color: #f44336;"> Entertainment & Nightlife</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        entertainment = [
            "Fun bars with live music tonight",
            "Rooftop bars with good views"
        ]
        
        for example in entertainment:
            st.markdown(f'<div class="example-query"> "{example}"</div>', unsafe_allow_html=True)
    
    with col2:
        entertainment_2 = [
            "Sports bars showing the game",
            "Craft beer bars in downtown area"
        ]
        
        for example in entertainment_2:
            st.markdown(f'<div class="example-query"> "{example}"</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Cuisine-Specific Section
    st.markdown("""
    <div class="example-section">
        <h3 style="margin-top: 0; color: #f44336;"> Cuisine-Specific</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        cuisine = [
            "Authentic Mexican tacos near me",
            "Best Thai food in the area"
        ]
        
        for example in cuisine:
            st.markdown(f'<div class="example-query"> "{example}"</div>', unsafe_allow_html=True)
    
    with col2:
        cuisine_2 = [
            "Korean BBQ restaurants with good reviews",
            "Indian restaurants with vegan options"
        ]
        
        for example in cuisine_2:
            st.markdown(f'<div class="example-query"> "{example}"</div>', unsafe_allow_html=True)

with tab3:
    st.markdown("## 📚 Citations Page")
    
    st.markdown("### Understanding Citations")
    
    st.markdown("""
    <div class="citation-box">
        <h4>Why Citations Matter</h4>
        <p>Every recommendation in Spotlight AI includes citations to original sources. This ensures:</p>
        <ul>
            <li><strong>Transparency:</strong> You can verify where information comes from</li>
            <li><strong>Trust:</strong> Our AI doesn't make things up - it's backed by real reviews</li>
            <li><strong>Exploration:</strong> You can dive deeper into specific aspects that interest you</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**Example Citation Format:**")
    st.markdown("""
    > "Great place to work! Quiet, fast WiFi, and the coffee is amazing."
    > 
    > *Source: Yelp Review by Sarah M., October 2024*
    """)
    
    st.divider()
    
    st.markdown("### How Citations Work")
    
    st.markdown("""
    When Spotlight AI generates a recommendation, it:
    
    1. **Retrieves relevant reviews** from Yelp and Google Places based on your query
    2. **Analyzes the content** using our RAG (Retrieval-Augmented Generation) pipeline
    3. **Generates a summary** that synthesizes information from multiple sources
    4. **Provides citations** linking back to the original reviews
    
    This approach ensures that every piece of information can be traced back to its source, 
    giving you confidence in the recommendations you receive.
    """)
    
    st.divider()
    
    st.markdown("### Data Sources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Yelp API**
        - Business information
        - User reviews and ratings
        - Photos and hours
        - Contact information
        """)
    
    with col2:
        st.markdown("""
        **Google Places API**
        - Location data
        - Additional reviews
        - Real-time information
        - Maps integration
        """)
    
    st.divider()
    
    st.markdown("### References")
    
    references = [
        "[1] Yelp, 'Yelp API,' https://www.yelp.com/developers",
        "[2] Kaggle, 'Yelp Dataset,' https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset",
        "[3] OpenAI, 'GPT-4 Technical Report,' 2023",
        "[4] Google, 'Google Places API,' https://developers.google.com/maps/documentation/places",
        "[5] LangChain, 'Framework for developing applications powered by language models,' https://www.langchain.com"
    ]
    
    for ref in references:
        st.caption(ref)

# Footer
