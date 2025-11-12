import streamlit as st
import hashlib
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Spotlight AI - Sign In",
    page_icon="🔦",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .auth-container {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        max-width: 450px;
        margin: 2rem auto;
    }
    .logo-text {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #5568d3 0%, #6a4193 100%);
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1rem;
    }
    .divider {
        text-align: center;
        margin: 2rem 0;
        color: #999;
    }
    .social-btn {
        width: 100%;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border: 2px solid #ddd;
        background: white;
        cursor: pointer;
        font-size: 1rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .feature-badge {
        background: #f0f0f0;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        display: inline-block;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False

# Mock user database (in production, use real database)
# Format: {email: {password_hash, name, created_at}}
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        # Demo user: email=demo@spotlight.ai, password=demo123
        'demo@spotlight.ai': {
            'password_hash': hashlib.sha256('demo123'.encode()).hexdigest(),
            'name': 'Demo User',
            'created_at': '2024-01-01'
        }
    }

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_login(email, password):
    if email in st.session_state.users_db:
        stored_hash = st.session_state.users_db[email]['password_hash']
        if hash_password(password) == stored_hash:
            return True, st.session_state.users_db[email]
    return False, None

def create_account(email, password, name):
    if email in st.session_state.users_db:
        return False, "Account already exists"
    
    st.session_state.users_db[email] = {
        'password_hash': hash_password(password),
        'name': name,
        'created_at': datetime.now().strftime('%Y-%m-%d')
    }
    return True, "Account created successfully"

# Main content
if not st.session_state.authenticated:
    # Branding header
    st.markdown('<div class="logo-text">🔦 Spotlight AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your Personal Local Search Assistant</div>', unsafe_allow_html=True)
    
    # Features preview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-badge">🤖 AI-Powered</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-badge">🎯 Personalized</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="feature-badge">📍 Real-Time</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Toggle between Sign In and Sign Up
    tab1, tab2 = st.tabs(["🔑 Sign In", "✨ Sign Up"])
    
    with tab1:
        st.markdown("### Welcome Back!")
        
        with st.form("signin_form"):
            email = st.text_input("Email", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns([3, 2])
            with col1:
                remember_me = st.checkbox("Remember me")
            with col2:
                st.markdown("[Forgot password?](#)")
            
            submit = st.form_submit_button("Sign In")
            
            if submit:
                if not email or not password:
                    st.error("Please fill in all fields")
                else:
                    success, user_data = verify_login(email, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_data = {
                            'email': email,
                            'name': user_data['name']
                        }
                        st.success(f"Welcome back, {user_data['name']}! 🎉")
                        st.balloons()
                        # Give user time to see success message
                        st.markdown("Redirecting to app...")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
        
        st.markdown('<div class="divider">OR</div>', unsafe_allow_html=True)
        
        # Social login buttons
        if st.button("🔍 Continue with Google", key="google_signin"):
            st.info("Google OAuth integration coming soon!")
        
        if st.button("📘 Continue with Facebook", key="fb_signin"):
            st.info("Facebook OAuth integration coming soon!")
        
        # Demo account info
        st.info("💡 **Try it now!** Use demo@spotlight.ai / demo123")
    
    with tab2:
        st.markdown("### Create Your Account")
        
        with st.form("signup_form"):
            name = st.text_input("Full Name", placeholder="John Doe")
            email = st.text_input("Email", placeholder="your.email@example.com", key="signup_email")
            password = st.text_input("Password", type="password", placeholder="Create a strong password", key="signup_pass")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
            
            agree = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            submit = st.form_submit_button("Create Account")
            
            if submit:
                if not name or not email or not password or not confirm_password:
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords don't match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters")
                elif not agree:
                    st.error("Please agree to the Terms of Service")
                else:
                    success, message = create_account(email, password, name)
                    if success:
                        st.success(f"{message} 🎉")
                        st.info("Please sign in with your new account")
                    else:
                        st.error(message)
        
        st.markdown('<div class="divider">OR</div>', unsafe_allow_html=True)
        
        # Social signup buttons
        if st.button("🔍 Sign up with Google", key="google_signup"):
            st.info("Google OAuth integration coming soon!")
        
        if st.button("📘 Sign up with Facebook", key="fb_signup"):
            st.info("Facebook OAuth integration coming soon!")

else:
    # User is authenticated - show main app
    st.markdown(f"# Welcome, {st.session_state.user_data['name']}! 👋")
    st.success("You're successfully signed in!")
    
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 What would you like to do?
    
    - 🔍 **Search** for local restaurants and cafes
    - ⭐ **Discover** hidden gems based on your preferences
    - 💬 **Chat** with AI to get personalized recommendations
    - 📍 **Explore** interactive maps of your area
    - ❤️ **Save** your favorite places
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Start Exploring", key="start_app"):
            st.info("Redirecting to main app...")
            # In production, navigate to your main app page
            st.markdown("This would redirect to your main Spotlight AI app (Homepage.py)")
    
    with col2:
        if st.button("⚙️ Preferences", key="preferences"):
            st.info("Opening preferences...")
    
    with col3:
        if st.button("🚪 Sign Out", key="signout"):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.rerun()
    
    st.markdown("---")
    
    # User profile preview
    with st.expander("👤 Your Profile"):
        st.write(f"**Name:** {st.session_state.user_data['name']}")
        st.write(f"**Email:** {st.session_state.user_data['email']}")
        st.write(f"**Member Since:** {st.session_state.users_db[st.session_state.user_data['email']]['created_at']}")
        
        if st.button("Edit Profile"):
            st.info("Profile editing coming soon!")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("[About]()")
with col2:
    st.markdown("[Privacy]()")
with col3:
    st.markdown("[Support]()")

st.markdown("<p style='text-align: center; color: #999; margin-top: 2rem;'>© 2024 Spotlight AI. Built with ❤️ by Howard, Zayba, and Tiana</p>", unsafe_allow_html=True)