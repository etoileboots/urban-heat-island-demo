import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Urban Heat Island NYC",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Check if this is first load using session state
if 'loaded' not in st.session_state:
    st.session_state.loaded = False

# Clean light mode CSS with fade-in animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Gotu&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #fff8f0 0%, #fff0e6 50%, #ffe8d6 100%);
    }
    
    [data-testid="stSidebar"] {
        background: rgba(255, 250, 245, 0.95);
        border-right: 1px solid #f0e6dc;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fade in animation */
    @keyframes fadeIn {
        0% {
            opacity: 0;
            transform: translateY(20px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 35vh;
        padding: 100px 20px 40px;
    }
    
    .hero-welcome {
        font-family: 'DM Sans', sans-serif;
        font-size: 2rem;
        font-weight: 400;
        color: #888;
        text-align: center;
        margin-bottom: 12px;
        opacity: 0;
        animation: fadeIn 1s ease-out forwards;
        animation-delay: 0.5s;
    }
    
    .hero-title {
        font-family: 'Gotu', serif;
        font-size: 9rem;
        font-weight: 400;
        color: #1a1a1a;
        text-align: center;
        letter-spacing: 0.02em;
        opacity: 0;
        animation: fadeIn 1s ease-out forwards;
        animation-delay: 1.8s;
    }
    
    .hero-subtitle {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.6rem;
        font-weight: 400;
        color: #888;
        text-align: center;
        margin-top: 20px;
        opacity: 0;
        animation: fadeIn 1s ease-out forwards;
        animation-delay: 3.0s;
    }
    
    /* Style the buttons as circular gradient cards */
    .stButton > button {
        font-family: 'DM Sans', sans-serif !important;
        background: radial-gradient(circle at center, rgba(249, 115, 22, 0.15) 0%, rgba(249, 115, 22, 0.08) 40%, transparent 70%) !important;
        border-radius: 50% !important;
        padding: 48px 32px !important;
        min-height: 240px !important;
        width: 240px !important;
        box-shadow: none !important;
        transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), background 0.4s ease !important;
        cursor: pointer !important;
        border: none !important;
        text-align: center !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        color: #1a1a1a !important;
        font-weight: 400 !important;
        white-space: pre-wrap !important;
        line-height: 1.5 !important;
        margin: 0 auto !important;
        opacity: 0;
        animation: fadeIn 1s ease-out forwards;
        animation-delay: 3.0s;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) !important;
        background: radial-gradient(circle at center, rgba(249, 115, 22, 0.25) 0%, rgba(249, 115, 22, 0.12) 40%, transparent 70%) !important;
        box-shadow: none !important;
        border: none !important;
    }
    
    .stButton > button:focus {
        box-shadow: none !important;
        outline: none !important;
        border: none !important;
    }
    
    .stButton > button:active {
        transform: scale(1.02) !important;
    }
    
    .stButton > button p {
        margin: 0 !important;
        text-align: center !important;
    }
    
    /* Style the number */
    .stButton > button strong {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        color: #f97316 !important;
        letter-spacing: 0.15em !important;
        display: block !important;
        margin-bottom: 12px !important;
    }
    
    /* Center the columns properly */
    [data-testid="column"] {
        display: flex !important;
        justify-content: center !important;
    }
    
    /* For already loaded state - show immediately */
    .loaded .stButton > button {
        opacity: 1 !important;
        animation: none !important;
    }
    
    .loaded .hero-welcome,
    .loaded .hero-title,
    .loaded .hero-subtitle {
        opacity: 1 !important;
        animation: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Add loaded class if returning to page
if st.session_state.loaded:
    st.markdown('<script>document.querySelector(".stApp").classList.add("loaded");</script>', unsafe_allow_html=True)

# Hero section with staggered fade-in
st.markdown("""
<div class="hero-container">
    <p class="hero-welcome">Welcome to the</p>
    <h1 class="hero-title">Urban Heat Island</h1>
    <p class="hero-subtitle">Exploring temperature disparities across New York City</p>
</div>
""", unsafe_allow_html=True)

# Navigation cards
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    c1, c2, c3 = st.columns(3, gap="large")
    
    with c1:
        card1_text = """**01**

Explore the
UHI Effect

→"""
        if st.button(card1_text, key="btn1", use_container_width=True):
            st.session_state.loaded = True
            st.switch_page("pages/1_Explore_UHI.py")
    
    with c2:
        card2_text = """**02**

Inequality
& UHI

→"""
        if st.button(card2_text, key="btn2", use_container_width=True):
            st.session_state.loaded = True
            st.switch_page("pages/2_Inequality_and_UHI.py")
    
    with c3:
        card3_text = """**03**

Mitigations
& Solutions

→"""
        if st.button(card3_text, key="btn3", use_container_width=True):
            st.session_state.loaded = True
            st.switch_page("pages/3_Mitigations_and_Solutions.py")

# Mark as loaded after first render
st.session_state.loaded = True
