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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        border-left: 5px solid #667eea;
    }
    .example-query {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
        font-family: monospace;
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
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 About", "📖 How to Use", "💡 Examples", "❓ FAQ", "👥 Team"])

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
            <h3>🤖 AI-Powered Intelligence</h3>
            <p>Our advanced RAG (Retrieval-Augmented Generation) pipeline analyzes thousands of reviews 
            to give you concise, relevant answers to your questions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Personalized Results</h3>
            <p>Spotlight AI learns your preferences over time - dietary restrictions, budget, atmosphere - 
            to provide increasingly tailored recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>📱 Real-Time Data</h3>
            <p>We integrate live data from Yelp and Google Places to ensure you always get current 
            information about hours, menus, and reviews.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>💬 Natural Conversation</h3>
            <p>Just ask questions in plain English. No need to navigate complex filters or 
            sort through endless reviews.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>📍 Location-Aware</h3>
            <p>Automatic location detection ensures recommendations are always relevant to where you are 
            or where you're going.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>✅ Transparent Citations</h3>
            <p>Every recommendation includes links to source reviews, so you can verify 
            and explore further with confidence.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 🔧 Technology Stack")
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
    st.markdown("## 📖 How to Use Spotlight AI")
    
    st.markdown("### 🚀 Getting Started")
    
    steps = [
        {
            "title": "1️⃣ Sign Up & Set Preferences",
            "desc": "Create an account and set your dietary preferences, budget range, and atmosphere preferences. This helps us personalize recommendations from day one."
        },
        {
            "title": "2️⃣ Ask Your Question",
            "desc": "Use the chat interface to ask about local places in natural language. Be specific about what you're looking for!"
        },
        {
            "title": "3️⃣ Review Recommendations",
            "desc": "Browse AI-generated recommendations with ratings, reviews, and key details. Each suggestion includes citations from real reviews."
        },
        {
            "title": "4️⃣ Provide Feedback",
            "desc": "Like, save, or dismiss recommendations. Your feedback helps us learn your preferences and improve future suggestions."
        },
        {
            "title": "5️⃣ Explore & Discover",
            "desc": "Use the map view, save favorites, and explore your history to keep track of places you want to try."
        }
    ]
    
    for step in steps:
        st.markdown(f"""
        <div class="feature-card">
            <h3>{step['title']}</h3>
            <p>{step['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 💡 Tips for Better Results")
    
    tips = [
        "**Be specific**: Instead of 'restaurants', try 'Italian restaurants with outdoor seating'",
        "**Mention constraints**: Include budget, distance, or time constraints in your query",
        "**Use context**: 'Date night spots' or 'study cafes' helps us understand the occasion",
        "**Update preferences**: Keep your profile updated to get increasingly accurate recommendations",
        "**Give feedback**: The more you interact, the smarter Spotlight AI becomes!"
    ]
    
    for tip in tips:
        st.markdown(f"✅ {tip}")

with tab3:
    st.markdown("## 💡 Example Queries")
    st.caption("Try these sample queries to see what Spotlight AI can do:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🍽️ Food & Dining")
        
        examples = [
            "Find me vegetarian restaurants under $20 near downtown",
            "What are the best brunch spots with outdoor seating?",
            "Show me highly-rated sushi restaurants within 5 miles",
            "Late night food options that are open now",
            "Italian restaurants good for a date night"
        ]
        
        for example in examples:
            st.markdown(f'<div class="example-query">💬 "{example}"</div>', unsafe_allow_html=True)
            if st.button(f"Try this", key=f"try_{example[:20]}"):
                st.info(f"Searching for: {example}")
        
        st.markdown("### ☕ Work & Study")
        
        work_examples = [
            "Quiet coffee shops with WiFi for working",
            "Study spots open late with good coffee",
            "Cafes with power outlets and comfortable seating"
        ]
        
        for example in work_examples:
            st.markdown(f'<div class="example-query">💬 "{example}"</div>', unsafe_allow_html=True)
            if st.button(f"Try this", key=f"try_work_{example[:20]}"):
                st.info(f"Searching for: {example}")
    
    with col2:
        st.markdown("### 🎉 Entertainment & Nightlife")
        
        entertainment = [
            "Fun bars with live music tonight",
            "Rooftop bars with good views",
            "Sports bars showing the game",
            "Craft beer bars in downtown area"
        ]
        
        for example in entertainment:
            st.markdown(f'<div class="example-query">💬 "{example}"</div>', unsafe_allow_html=True)
            if st.button(f"Try this", key=f"try_ent_{example[:20]}"):
                st.info(f"Searching for: {example}")
        
        st.markdown("### 🌮 Cuisine-Specific")
        
        cuisine = [
            "Authentic Mexican tacos near me",
            "Best Thai food in the area",
            "Korean BBQ restaurants with good reviews",
            "Indian restaurants with vegan options"
        ]
        
        for example in cuisine:
            st.markdown(f'<div class="example-query">💬 "{example}"</div>', unsafe_allow_html=True)
            if st.button(f"Try this", key=f"try_cuisine_{example[:20]}"):
                st.info(f"Searching for: {example}")

with tab4:
    st.markdown("## ❓ Frequently Asked Questions")
    
    faqs = [
        {
            "q": "How does Spotlight AI generate recommendations?",
            "a": "Spotlight AI uses Retrieval-Augmented Generation (RAG) to analyze reviews from Yelp and Google Places. We retrieve relevant reviews, process them with AI, and generate personalized recommendations based on your preferences and the context of your query."
        },
        {
            "q": "Is my data private and secure?",
            "a": "Yes! Your search history, preferences, and saved places are stored securely and never shared with third parties. You can export or delete your data at any time from your profile settings."
        },
        {
            "q": "How are citations generated?",
            "a": "Every recommendation includes citations linking back to the original reviews we analyzed. This ensures transparency and allows you to verify the information and read more details if needed."
        },
        {
            "q": "Can I use Spotlight AI in different cities?",
            "a": "Absolutely! Spotlight AI works wherever Yelp and Google Places data is available. Just update your location in preferences or mention the city in your query."
        },
        {
            "q": "How does personalization work?",
            "a": "The more you use Spotlight AI, the better it understands your preferences. We track your saved places, feedback (likes/dislikes), dietary restrictions, and search patterns to provide increasingly tailored recommendations."
        },
        {
            "q": "What if I find incorrect information?",
            "a": "While we strive for accuracy, data is sourced from third-party platforms and may occasionally be outdated. You can report issues through our feedback system, and we'll investigate promptly."
        },
        {
            "q": "Is there a mobile app?",
            "a": "Currently, Spotlight AI is web-based and mobile-responsive. A dedicated mobile app is in our roadmap for future releases!"
        },
        {
            "q": "How do I export my saved places?",
            "a": "Go to the 'History & Saved Places' page and click the 'Export List' button to download your saved places as a CSV file."
        }
    ]
    
    for faq in faqs:
        with st.expander(f"**{faq['q']}**"):
            st.markdown(faq['a'])
    
    st.divider()
    
    st.markdown("""
    ### 📧 Still Have Questions?
    
    Can't find what you're looking for? Contact our support team:
    - Email: support@spotlightai.com
    - Twitter: @SpotlightAI
    - GitHub: github.com/spotlight-ai
    """)
    
    st.markdown("### 📚 Understanding Citations")
    
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

with tab5:
    st.markdown("## 👥 Meet the Team")
    
    st.markdown("""
    Spotlight AI is a student project created at San Jose State University as part of our Computer Science program.
    We're passionate about using AI to solve real-world problems and make everyday decisions easier.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="team-card">
            <div style="font-size: 4rem;">👨‍💻</div>
            <h3>Howard Wei</h3>
            <p style="color: #667eea; font-weight: bold;">Backend & RAG Pipeline</p>
            <p style="color: #6c757d; font-size: 14px;">
                howard.wei@sjsu.edu<br>
                Department of Computer Science<br>
                San Jose State University
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="team-card">
            <div style="font-size: 4rem;">👩‍💻</div>
            <h3>Zayba Syed</h3>
            <p style="color: #667eea; font-weight: bold;">API Integration & Data</p>
            <p style="color: #6c757d; font-size: 14px;">
                zayba.syed@sjsu.edu<br>
                Department of Computer Science<br>
                San Jose State University
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="team-card">
            <div style="font-size: 4rem;">👩‍💻</div>
            <h3>Tiana Phung</h3>
            <p style="color: #667eea; font-weight: bold;">Frontend & UI/UX</p>
            <p style="color: #6c757d; font-size: 14px;">
                tiana.phung@sjsu.edu<br>
                Department of Computer Science<br>
                San Jose State University
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 🎓 Project Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🏫 Institution:**  
        San Jose State University
        
        **📚 Course:**  
        Advanced Topics in Computer Science
        
        **📅 Project Duration:**  
        3 Months (Sept - Nov 2024)
        """)
    
    with col2:
        st.markdown("""
        **🔗 Resources:**
        - [GitHub Repository](#)
        - [Project Documentation](#)
        - [Demo Video](#)
        - [Research Paper](#)
        """)
    
    st.divider()
    
    st.markdown("### 📖 References")
    
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
st.divider()
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem 0;">
    <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">🔦 Spotlight AI</p>
    <p style="font-size: 0.9rem;">Built with ❤️ by Howard Wei, Zayba Syed, and Tiana Phung</p>
    <p style="font-size: 0.8rem;">© 2024 San Jose State University • All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)