"""
🎓 AI Personalized Learning System
Main Streamlit Application
"""
import streamlit as st
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from utils.db import init_db, login_user, register_user, update_streak, get_streak
from modules.quiz_engine import get_all_topics, get_topic_stats

# Page configuration
st.set_page_config(
    page_title="EduAI — Personalized Learning",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://github.com",
        "About": "EduAI — AI-Powered Personalized Learning System"
    }
)

# Initialize database
init_db()

# ─── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* Global Reset */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0D0D1A;
    font-family: 'Inter', sans-serif;
    color: #E0E0FF;
}

/* Hide default streamlit UI */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* Main container */
[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(135deg, #0D0D1A 0%, #1A1A2E 50%, #0F0F23 100%);
    min-height: 100vh;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12122A 0%, #1A1A38 100%) !important;
    border-right: 1px solid rgba(108, 99, 255, 0.2);
}

[data-testid="stSidebar"] .stRadio > div {
    gap: 4px;
}

/* Cards */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(108,99,255,0.25);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.glass-card:hover {
    border-color: rgba(108,99,255,0.5);
    background: rgba(255,255,255,0.06);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(108,99,255,0.15);
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, rgba(108,99,255,0.15), rgba(108,99,255,0.05));
    border: 1px solid rgba(108,99,255,0.3);
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6C63FF, #9C92FF) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(108,99,255,0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(108,99,255,0.5) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(108,99,255,0.3) !important;
    border-radius: 10px !important;
    color: #E0E0FF !important;
    font-family: 'Inter', sans-serif !important;
}

.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(108,99,255,0.3) !important;
    border-radius: 10px !important;
    color: #E0E0FF !important;
}

/* Progress bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #6C63FF, #9C92FF) !important;
    border-radius: 8px !important;
}

/* Radio buttons */
.stRadio > div > label {
    color: #C0C0FF !important;
    font-size: 15px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid rgba(108,99,255,0.2);
}

.stTabs [data-baseweb="tab"] {
    color: #A0A0CC !important;
    border-radius: 8px !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6C63FF, #9C92FF) !important;
    color: white !important;
}

/* Alerts / Info boxes */
.stAlert {
    border-radius: 12px !important;
    border: none !important;
}

/* Headers */
h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #E0E0FF !important;
}

/* Divider */
hr { border-color: rgba(108,99,255,0.2) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0D0D1A; }
::-webkit-scrollbar-thumb { background: #6C63FF; border-radius: 3px; }

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, rgba(108,99,255,0.2) 0%, rgba(156,146,255,0.1) 50%, rgba(108,99,255,0.05) 100%);
    border: 1px solid rgba(108,99,255,0.3);
    border-radius: 24px;
    padding: 40px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(108,99,255,0.05) 0%, transparent 70%);
    animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

/* Badge */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

.badge-beginner { background: rgba(255,107,107,0.2); color: #FF6B6B; border: 1px solid rgba(255,107,107,0.4); }
.badge-intermediate { background: rgba(255,217,61,0.2); color: #FFD93D; border: 1px solid rgba(255,217,61,0.4); }
.badge-advanced { background: rgba(107,203,119,0.2); color: #6BCB77; border: 1px solid rgba(107,203,119,0.4); }

/* Chat bubble */
.chat-user {
    background: linear-gradient(135deg, rgba(108,99,255,0.25), rgba(108,99,255,0.1));
    border: 1px solid rgba(108,99,255,0.3);
    border-radius: 18px 4px 18px 18px;
    padding: 12px 18px;
    margin: 8px 0;
    max-width: 80%;
    margin-left: auto;
    color: #E0E0FF;
}

.chat-bot {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 4px 18px 18px 18px;
    padding: 12px 18px;
    margin: 8px 0;
    max-width: 85%;
    color: #E0E0FF;
}

/* Leaderboard row */
.leaderboard-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    border-radius: 10px;
    margin: 6px 0;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(108,99,255,0.15);
    transition: all 0.2s ease;
}

.leaderboard-row:hover {
    background: rgba(108,99,255,0.1);
    border-color: rgba(108,99,255,0.3);
}

/* Topic pill */
.topic-pill {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    margin: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
}

/* Correct/Wrong answer */
.correct-answer {
    background: rgba(107,203,119,0.15);
    border: 1px solid rgba(107,203,119,0.4);
    border-radius: 10px;
    padding: 8px 16px;
    color: #6BCB77;
}

.wrong-answer {
    background: rgba(255,107,107,0.15);
    border: 1px solid rgba(255,107,107,0.4);
    border-radius: 10px;
    padding: 8px 16px;
    color: #FF6B6B;
}
</style>
""", unsafe_allow_html=True)


# ─── Session State Init ───────────────────────────────────────────────────────
def init_session():
    defaults = {
        "logged_in": False,
        "user": None,
        "current_page": "🏠 Dashboard",
        "quiz_state": None,
        "chat_messages": [],
        "quiz_topic": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_session()


# ─── Auth Pages ───────────────────────────────────────────────────────────────
def show_login_page():
    st.markdown("""
    <div style="max-width: 480px; margin: 40px auto;">
        <div class="hero-banner" style="margin-bottom: 32px;">
            <h1 style="font-size: 42px; margin: 0; background: linear-gradient(135deg, #6C63FF, #C0C0FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🎓 EduAI
            </h1>
            <p style="color: #A0A0CC; margin-top: 8px; font-size: 16px;">
                Your AI-Powered Personalized Learning Companion
            </p>
            <div style="display: flex; justify-content: center; gap: 16px; margin-top: 16px; flex-wrap: wrap;">
                <span style="color: #6C63FF; font-size: 13px;">📊 Progress Tracking</span>
                <span style="color: #9C92FF; font-size: 13px;">🧠 NLP Analysis</span>
                <span style="color: #6C63FF; font-size: 13px;">🤖 AI Tutor</span>
                <span style="color: #9C92FF; font-size: 13px;">🎯 Adaptive Quizzes</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_register = st.tabs(["🔐 Login", "✨ Register"])

        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            username = st.text_input("Username", key="login_user", placeholder="Enter your username")
            password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")
            
            if st.button("Login →", key="login_btn", use_container_width=True):
                if username and password:
                    success, user = login_user(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        update_streak(user["id"])
                        st.success(f"Welcome back, {user['full_name']}! 🎉")
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")
                else:
                    st.warning("Please fill in all fields.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background: rgba(108,99,255,0.1); border-radius: 10px; padding: 12px; text-align: center; border: 1px solid rgba(108,99,255,0.2);">
                <p style="color: #A0A0CC; font-size: 13px; margin: 0;">
                    🚀 Demo: <strong style="color: #9C92FF;">demo</strong> / <strong style="color: #9C92FF;">demo123</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)

        with tab_register:
            st.markdown("<br>", unsafe_allow_html=True)
            full_name = st.text_input("Full Name", key="reg_name", placeholder="Your full name")
            email = st.text_input("Email", key="reg_email", placeholder="your@email.com")
            new_user = st.text_input("Username", key="reg_user", placeholder="Choose a username")
            new_pass = st.text_input("Password", type="password", key="reg_pass", placeholder="Create a password")
            confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Repeat password")

            if st.button("Create Account →", key="register_btn", use_container_width=True):
                if not all([full_name, email, new_user, new_pass, confirm_pass]):
                    st.warning("Please fill in all fields.")
                elif new_pass != confirm_pass:
                    st.error("Passwords don't match.")
                elif len(new_pass) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    success, user_id = register_user(new_user, new_pass, full_name, email)
                    if success:
                        st.success("Account created! Please login. 🎉")
                    else:
                        st.error("Username already taken. Choose another.")


# ─── Sidebar ─────────────────────────────────────────────────────────────────
def show_sidebar():
    user = st.session_state.user
    streak = get_streak(user["id"])

    with st.sidebar:
        # User profile
        avatar_color = user.get("avatar_color", "#6C63FF")
        initials = "".join([n[0].upper() for n in user["full_name"].split()[:2]])
        
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 10px;">
            <div style="width: 70px; height: 70px; border-radius: 50%; 
                background: linear-gradient(135deg, {avatar_color}, #9C92FF); 
                display: flex; align-items: center; justify-content: center;
                margin: 0 auto 12px; font-size: 24px; font-weight: 700; color: white;
                box-shadow: 0 4px 20px rgba(108,99,255,0.4);">
                {initials}
            </div>
            <div style="font-weight: 700; font-size: 16px; color: #E0E0FF;">{user['full_name']}</div>
            <div style="color: #7070AA; font-size: 13px;">@{user['username']}</div>
            <div style="margin-top: 12px; display: flex; justify-content: center; gap: 16px;">
                <div style="text-align: center;">
                    <div style="font-size: 20px; font-weight: 700; color: #FFD93D;">🔥 {streak['current_streak']}</div>
                    <div style="font-size: 11px; color: #7070AA;">Streak</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 20px; font-weight: 700; color: #6BCB77;">📅 {streak['total_study_days']}</div>
                    <div style="font-size: 11px; color: #7070AA;">Days</div>
                </div>
            </div>
        </div>
        <hr style="border-color: rgba(108,99,255,0.2); margin: 0 0 16px;">
        """, unsafe_allow_html=True)

        # Navigation
        pages = [
            "🏠 Dashboard",
            "📝 Take Quiz",
            "📊 Analytics",
            "🎯 Recommendations",
            "🤖 AI Tutor",
            "🏆 Leaderboard",
        ]
        
        st.markdown("<div style='font-size: 11px; font-weight: 600; color: #5050AA; letter-spacing: 1px; padding: 0 4px 8px;'>NAVIGATION</div>", unsafe_allow_html=True)
        
        selected = st.radio(
            "nav", pages,
            index=pages.index(st.session_state.current_page) if st.session_state.current_page in pages else 0,
            label_visibility="collapsed"
        )
        st.session_state.current_page = selected

        st.markdown("<hr style='border-color: rgba(108,99,255,0.2);'>", unsafe_allow_html=True)
        
        # Topics mini overview
        stats = get_topic_stats()
        st.markdown("<div style='font-size: 11px; font-weight: 600; color: #5050AA; letter-spacing: 1px; padding: 0 4px 8px;'>SUBJECTS</div>", unsafe_allow_html=True)
        topic_emojis = {"Mathematics": "📐", "Physics": "⚛️", "Computer Science": "💻", "Chemistry": "🧪", "Biology": "🧬"}
        for topic, count in stats.items():
            emoji = topic_emojis.get(topic, "📚")
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; 
                padding: 6px 8px; margin: 3px 0; border-radius: 8px;
                background: rgba(255,255,255,0.03);">
                <span style="font-size: 13px; color: #C0C0FF;">{emoji} {topic}</span>
                <span style="font-size: 11px; color: #6C63FF; font-weight: 600;">{count}Q</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ─── Page Router ─────────────────────────────────────────────────────────────
def main():
    if not st.session_state.logged_in:
        show_login_page()
        return

    show_sidebar()

    page = st.session_state.current_page

    if page == "🏠 Dashboard":
        from pages_content.dashboard import show_dashboard
        show_dashboard()
    elif page == "📝 Take Quiz":
        from pages_content.quiz import show_quiz
        show_quiz()
    elif page == "📊 Analytics":
        from pages_content.analytics import show_analytics
        show_analytics()
    elif page == "🎯 Recommendations":
        from pages_content.recommendations import show_recommendations
        show_recommendations()
    elif page == "🤖 AI Tutor":
        from pages_content.chatbot_ui import show_chatbot
        show_chatbot()
    elif page == "🏆 Leaderboard":
        from pages_content.leaderboard import show_leaderboard
        show_leaderboard()


if __name__ == "__main__":
    # Ensure demo user exists
    from utils.db import get_all_usernames
    existing = get_all_usernames()
    if "demo" not in existing:
        register_user("demo", "demo123", "Demo Student", "demo@eduai.com")
        # Seed some demo data
        from utils.db import save_quiz_session, update_topic_performance
        topics_scores = [
            ("Mathematics", 72, 10, 7, 420, "medium"),
            ("Physics", 55, 8, 4, 380, "medium"),
            ("Computer Science", 88, 12, 10, 510, "hard"),
            ("Chemistry", 40, 8, 3, 360, "easy"),
            ("Biology", 65, 10, 6, 400, "medium"),
        ]
        from utils.db import login_user
        _, demo_user = login_user("demo", "demo123")
        if demo_user:
            for topic, score, total, correct, time_taken, diff in topics_scores:
                sid = save_quiz_session(demo_user["id"], topic, score, total, correct, time_taken, diff)
                update_topic_performance(demo_user["id"], topic, score)
    
    main()
