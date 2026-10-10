"""
AI Chatbot Tutor Page
"""
import streamlit as st
from datetime import datetime

from modules.chatbot import get_bot_response
from utils.db import save_chat_message, get_chat_history, get_user_performance
from modules.recommender import get_adaptive_difficulty


def show_chatbot():
    user = st.session_state.user
    performance = get_user_performance(user["id"])

    st.markdown("""
    <h1 style="background: linear-gradient(135deg, #6C63FF, #C0C0FF); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        font-family: 'Space Grotesk', sans-serif; margin-bottom: 8px;">
        🤖 AI Tutor
    </h1>
    <p style="color: #7070AA; margin-bottom: 16px;">
        Your personal AI teaching assistant — ask anything about STEM subjects
    </p>
    """, unsafe_allow_html=True)

    col_chat, col_sidebar = st.columns([3, 1])

    with col_sidebar:
        # Topic context selector
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 16px;">
            <div style="font-weight: 600; color: #9C92FF; margin-bottom: 12px;">⚙️ Context</div>
        </div>
        """, unsafe_allow_html=True)

        topics = ["None (General)", "Mathematics", "Physics", "Computer Science", "Chemistry", "Biology"]
        topic_ctx = st.selectbox("Current Subject", topics, key="chat_topic")
        topic_context = "" if topic_ctx == "None (General)" else topic_ctx

        # Score for hints
        topic_perf = next((p for p in performance if p["topic"] == topic_context), None)
        topic_score = topic_perf["proficiency_score"] if topic_perf else 50.0

        # Quick questions
        st.markdown("""
        <div style="font-size: 12px; font-weight: 600; color: #5050AA; letter-spacing: 1px; margin: 16px 0 8px;">
            QUICK TOPICS
        </div>
        """, unsafe_allow_html=True)

        quick_questions = {
            "📐 Math": "Explain derivatives and integrals",
            "⚛️ Physics": "Explain Newton's laws of motion",
            "💻 CS": "What is Big O notation?",
            "🧬 Bio": "Explain DNA and photosynthesis",
            "🧪 Chem": "Explain acids and bases",
            "🔄 OOP": "Explain OOP concepts",
            "🔁 Recursion": "What is recursion?",
            "📊 Stats": "Explain probability",
        }

        for label, question in quick_questions.items():
            if st.button(label, key=f"quick_q_{label}", use_container_width=True):
                # Add to message queue
                if "pending_message" not in st.session_state:
                    st.session_state.pending_message = None
                st.session_state.pending_message = question
                st.rerun()

        st.markdown("<hr style='border-color: rgba(108,99,255,0.2);'>", unsafe_allow_html=True)

        if st.button("🗑️ Clear Chat", use_container_width=True, key="clear_chat"):
            st.session_state.chat_messages = []
            st.rerun()

        # Stats
        st.markdown(f"""
        <div style="background: rgba(108,99,255,0.08); border: 1px solid rgba(108,99,255,0.2); 
            border-radius: 10px; padding: 12px; margin-top: 8px;">
            <div style="font-size: 12px; color: #7070AA;">Messages</div>
            <div style="font-size: 24px; font-weight: 700; color: #6C63FF;">
                {len(st.session_state.chat_messages)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_chat:
        # Initialize chat from database or with welcome message
        if not st.session_state.chat_messages:
            history = get_chat_history(user["id"])
            if history:
                st.session_state.chat_messages = [
                    {
                        "role": h["role"],
                        "content": h["message"],
                        "timestamp": (h.get("timestamp") or "")[11:16] if h.get("timestamp") else ""
                    }
                    for h in history
                ]
            else:
                welcome = "Hello! I'm your AI Tutor 🤖\n\nI can help you with:\n- Mathematics (Calculus, Algebra, Statistics)\n- Physics (Mechanics, Quantum, Thermodynamics)\n- Computer Science (Algorithms, ML, OOP)\n- Chemistry (Organic, Physical, Thermodynamics)\n- Biology (Cell Biology, Genetics, Ecology)\n\nJust ask me anything! Try: *'Explain Newton's laws'* or *'What is Big O notation?'*"
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": welcome,
                    "timestamp": datetime.now().strftime("%H:%M")
                })

        # Chat display area
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_messages:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin: 8px 0;">
                        <div>
                            <div style="font-size: 11px; color: #5050AA; text-align: right; margin-bottom: 4px;">
                                You · {msg.get('timestamp', '')}
                            </div>
                            <div class="chat-user">{msg['content']}</div>
                        </div>
                        <div style="width: 36px; height: 36px; border-radius: 50%; 
                            background: linear-gradient(135deg, #6C63FF, #9C92FF);
                            display: flex; align-items: center; justify-content: center;
                            margin-left: 10px; flex-shrink: 0; font-size: 16px;">
                            👤
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="display: flex; margin: 8px 0;">
                        <div style="width: 36px; height: 36px; border-radius: 50%; 
                            background: linear-gradient(135deg, #1A1A2E, #2D2D5E);
                            border: 2px solid rgba(108,99,255,0.4);
                            display: flex; align-items: center; justify-content: center;
                            margin-right: 10px; flex-shrink: 0; font-size: 18px;">
                            🤖
                        </div>
                        <div>
                            <div style="font-size: 11px; color: #5050AA; margin-bottom: 4px;">
                                AI Tutor · {msg.get('timestamp', '')}
                            </div>
                            <div class="chat-bot" style="white-space: pre-wrap;">{msg['content']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # Handle pending messages from quick buttons
        if st.session_state.get("pending_message"):
            user_msg = st.session_state.pending_message
            st.session_state.pending_message = None

            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_msg,
                "timestamp": datetime.now().strftime("%H:%M")
            })

            with st.spinner("🤔 Thinking..."):
                bot_response = get_bot_response(user_msg, topic_context, topic_score)

            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": bot_response,
                "timestamp": datetime.now().strftime("%H:%M")
            })

            save_chat_message(user["id"], "user", user_msg)
            save_chat_message(user["id"], "assistant", bot_response)
            st.rerun()

        # Input area
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.form("chat_form", clear_on_submit=True):
            col_input, col_send = st.columns([5, 1])
            with col_input:
                user_input = st.text_input(
                    "Message",
                    placeholder="Ask me anything... 'What is recursion?', 'Explain photosynthesis', etc.",
                    label_visibility="collapsed",
                    key="chat_input"
                )
            with col_send:
                submitted = st.form_submit_button("Send →", use_container_width=True)

        if submitted and user_input.strip():
            msg_text = user_input.strip()
            ts = datetime.now().strftime("%H:%M")

            st.session_state.chat_messages.append({
                "role": "user",
                "content": msg_text,
                "timestamp": ts
            })

            bot_response = get_bot_response(msg_text, topic_context, topic_score)

            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": bot_response,
                "timestamp": datetime.now().strftime("%H:%M")
            })

            save_chat_message(user["id"], "user", msg_text)
            save_chat_message(user["id"], "assistant", bot_response)
            st.rerun()
