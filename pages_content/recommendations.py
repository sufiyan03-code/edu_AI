"""
Recommendations Page — Personalized learning path and resources
"""
import streamlit as st
import plotly.graph_objects as go

from utils.db import get_user_performance
from modules.recommender import generate_recommendations, get_learning_path, get_proficiency_label


def show_recommendations():
    user = st.session_state.user

    st.markdown("""
    <h1 style="background: linear-gradient(135deg, #6C63FF, #C0C0FF); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        font-family: 'Space Grotesk', sans-serif; margin-bottom: 8px;">
        🎯 Personalized Recommendations
    </h1>
    <p style="color: #7070AA; margin-bottom: 24px;">
        AI-generated learning path tailored to your performance
    </p>
    """, unsafe_allow_html=True)

    performance = get_user_performance(user["id"])
    rec = generate_recommendations(performance)
    path = get_learning_path(performance)

    # Study tip banner
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(108,99,255,0.2), rgba(156,146,255,0.1));
        border: 1px solid rgba(108,99,255,0.3); border-radius: 14px; padding: 20px; margin-bottom: 24px;
        display: flex; align-items: center; gap: 16px;">
        <div style="font-size: 36px;">💡</div>
        <div>
            <div style="font-weight: 600; color: #9C92FF; font-size: 14px; margin-bottom: 4px;">AI Study Tip</div>
            <div style="color: #E0E0FF; font-size: 15px;">{rec['study_tip']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_path, col_rec = st.columns([3, 2])

    with col_path:
        st.markdown("### 🗺️ Your Learning Path")

        status_icons = {
            "completed": ("✅", "#6BCB77", "Mastered"),
            "in_progress": ("🔄", "#FFD93D", "In Progress"),
            "not_started": ("⭕", "#5050AA", "Not Started"),
        }

        for step in path:
            icon, color, status_label = status_icons[step["status"]]
            score = step["score"]
            topic_emojis = {"Mathematics": "📐", "Physics": "⚛️", "Computer Science": "💻",
                            "Chemistry": "🧪", "Biology": "🧬"}
            t_emoji = topic_emojis.get(step["topic"], "📚")
            label, badge_color, badge_emoji = get_proficiency_label(score)

            st.markdown(f"""
            <div class="glass-card" style="margin-bottom: 12px; padding: 18px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="font-size: 28px;">{icon}</div>
                    <div style="flex: 1;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="font-weight: 600; color: #E0E0FF; font-size: 15px;">
                                {t_emoji} {step['topic']}
                            </div>
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="font-size: 11px; color: {badge_color}; background: rgba(255,255,255,0.05);
                                    padding: 3px 10px; border-radius: 20px; border: 1px solid {badge_color}44;">
                                    {badge_emoji} {label}
                                </span>
                                <span style="font-weight: 700; color: {color}; font-size: 16px;">{score:.0f}%</span>
                            </div>
                        </div>
                        <div style="color: {color}; font-size: 12px; margin-top: 4px;">{status_label}</div>
                        <div style="background: rgba(255,255,255,0.05); border-radius: 4px; height: 6px; margin-top: 8px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, {badge_color}, {badge_color}88); 
                                width: {score}%; height: 100%; border-radius: 4px;"></div>
                        </div>
                    </div>
                </div>
                <div style="margin-top: 12px; display: flex; gap: 8px;">
            """, unsafe_allow_html=True)

            cols = st.columns([3, 1])
            with cols[1]:
                if st.button(f"📝 Quiz", key=f"rec_quiz_{step['topic']}"):
                    st.session_state.quiz_topic = step["topic"]
                    st.session_state.current_page = "📝 Take Quiz"
                    st.rerun()

            st.markdown("</div></div>", unsafe_allow_html=True)

    with col_rec:
        st.markdown("### 📚 Suggested Resources")

        if not performance:
            st.info("Take quizzes to get personalized resource recommendations!")
        else:
            suggested = rec.get("suggested_content", {})

            for topic, content in suggested.items():
                level = content.get("level", "beginner")
                score = content.get("score", 0)
                resources = content.get("resources", [])
                color = "#FF6B6B" if level == "beginner" else "#FFD93D" if level == "intermediate" else "#6BCB77"
                
                topic_emojis = {"Mathematics": "📐", "Physics": "⚛️", "Computer Science": "💻",
                                "Chemistry": "🧪", "Biology": "🧬"}
                emoji = topic_emojis.get(topic, "📚")

                with st.expander(f"{emoji} {topic} — {level.title()} Resources", expanded=level == "beginner"):
                    if resources:
                        for r in resources:
                            st.markdown(f"""
                            <div style="padding: 8px 12px; margin: 4px 0; border-radius: 8px;
                                background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
                                font-size: 14px; color: #C0C0FF;">
                                📖 {r}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='color: #5050AA; font-size: 13px;'>No specific resources yet.</div>", unsafe_allow_html=True)

        # Priority recommendation
        if rec.get("priority_topics"):
            st.markdown("### 🔥 Priority Topics")
            st.markdown("""
            <div style="color: #7070AA; font-size: 13px; margin-bottom: 12px;">
                Focus on these topics for maximum improvement:
            </div>
            """, unsafe_allow_html=True)
            
            for i, topic in enumerate(rec["priority_topics"][:3]):
                priority_colors = ["#FF6B6B", "#FFD93D", "#9C92FF"]
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
                    border-left: 4px solid {priority_colors[i]}; border-radius: 8px; padding: 12px 16px; margin: 6px 0;">
                    <span style="color: {priority_colors[i]}; font-weight: 700;">#{i+1}</span>
                    <span style="color: #E0E0FF; margin-left: 8px; font-size: 14px;">{topic}</span>
                </div>
                """, unsafe_allow_html=True)

        # Next Steps
        if rec.get("next_steps"):
            st.markdown("### 📋 Action Plan")
            for step in rec["next_steps"]:
                st.markdown(f"""
                <div style="padding: 10px 14px; margin: 6px 0; border-radius: 8px;
                    background: rgba(108,99,255,0.08); border: 1px solid rgba(108,99,255,0.2);
                    font-size: 14px; color: #C0C0FF;">
                    ➡️ {step}
                </div>
                """, unsafe_allow_html=True)
