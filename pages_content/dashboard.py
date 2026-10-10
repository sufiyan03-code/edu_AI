"""
Dashboard Page — Overview of student performance (pandas-free version)
"""
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

from utils.db import get_user_performance, get_quiz_history, get_streak


def show_dashboard():
    user = st.session_state.user

    hour = datetime.now().hour
    greeting = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 17 else "Good Evening"

    st.markdown(f"""
    <div class="hero-banner" style="margin-bottom: 32px;">
        <h1 style="font-size: 36px; margin: 0; background: linear-gradient(135deg, #6C63FF, #C0C0FF); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family: 'Space Grotesk', sans-serif;">
            {greeting}, {user['full_name'].split()[0]}! 👋
        </h1>
        <p style="color: #A0A0CC; margin-top: 8px; font-size: 16px;">
            Ready to learn something amazing today?
        </p>
    </div>
    """, unsafe_allow_html=True)

    performance = get_user_performance(user["id"])
    quiz_history = get_quiz_history(user["id"])
    streak = get_streak(user["id"])

    avg_score = sum(p["proficiency_score"] for p in performance) / len(performance) if performance else 0
    total_quizzes = len(quiz_history)
    topics_attempted = len(performance)

    col1, col2, col3, col4 = st.columns(4)

    def metric_card(col, emoji, value, label, color, delta=None):
        with col:
            delta_html = f"<div style='font-size: 12px; color: {color}; margin-top: 4px;'>{delta}</div>" if delta else ""
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 32px;">{emoji}</div>
                <div style="font-size: 28px; font-weight: 800; color: {color}; line-height: 1.2;">{value}</div>
                <div style="font-size: 13px; color: #7070AA; margin-top: 4px;">{label}</div>
                {delta_html}
            </div>
            """, unsafe_allow_html=True)

    metric_card(col1, "🎯", f"{avg_score:.1f}%", "Overall Score", "#6C63FF", "↑ Keep going!")
    metric_card(col2, "📝", str(total_quizzes), "Quizzes Taken", "#9C92FF", f"{topics_attempted} topics")
    metric_card(col3, "🔥", str(streak.get("current_streak", 0)), "Day Streak", "#FFD93D", f"Best: {streak.get('longest_streak',0)}")
    metric_card(col4, "📅", str(streak.get("total_study_days", 0)), "Study Days", "#6BCB77", "Total active days")

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    TOPIC_COLORS = {
        "Mathematics": "#6C63FF", "Physics": "#FF6B6B",
        "Computer Science": "#6BCB77", "Chemistry": "#FFD93D", "Biology": "#FF8B94"
    }

    with col_left:
        st.markdown("### 📈 Score Progression")
        if quiz_history:
            # Group by topic
            topic_sessions = {}
            for s in sorted(quiz_history, key=lambda x: x["session_date"] or ""):
                t = s["topic"]
                if t not in topic_sessions:
                    topic_sessions[t] = {"dates": [], "scores": []}
                topic_sessions[t]["dates"].append((s.get("session_date") or "")[:16])
                topic_sessions[t]["scores"].append(s["score"])

            fig = go.Figure()
            for topic, data in topic_sessions.items():
                color = TOPIC_COLORS.get(topic, "#6C63FF")
                fig.add_trace(go.Scatter(
                    x=data["dates"], y=data["scores"],
                    mode="lines+markers",
                    name=topic,
                    marker=dict(size=8, color=color),
                    line=dict(color=color, width=2),
                ))

            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#A0A0CC"),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", range=[0, 105]),
                legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(108,99,255,0.3)"),
                margin=dict(l=0, r=0, t=10, b=0), height=300,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 60px; color: #5050AA;">
                <div style="font-size: 48px;">📊</div>
                <div style="margin-top: 12px;">Take your first quiz to see progress here!</div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown("### 🎯 Topic Mastery")
        if performance and len(performance) >= 2:
            topics = [p["topic"] for p in performance]
            scores = [p["proficiency_score"] for p in performance]
            topics_closed = topics + [topics[0]]
            scores_closed = scores + [scores[0]]

            fig2 = go.Figure()
            fig2.add_trace(go.Scatterpolar(
                r=scores_closed, theta=topics_closed,
                fill='toself', fillcolor='rgba(108,99,255,0.2)',
                line=dict(color='#6C63FF', width=2),
                marker=dict(size=6, color='#9C92FF'), name="Your Score"
            ))
            fig2.add_trace(go.Scatterpolar(
                r=[70] * len(topics_closed), theta=topics_closed,
                name="Target (70%)",
                line=dict(color='rgba(255,217,61,0.5)', width=1.5, dash='dash'),
            ))
            fig2.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)", color="#5050AA"),
                    angularaxis=dict(gridcolor="rgba(255,255,255,0.1)", color="#A0A0CC"),
                ),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#A0A0CC"), legend=dict(bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=0, r=0, t=10, b=0), height=300,
            )
            st.plotly_chart(fig2, use_container_width=True)
        elif performance:
            # Single topic — bar chart
            topics = [p["topic"] for p in performance]
            scores = [p["proficiency_score"] for p in performance]
            colors = [TOPIC_COLORS.get(t, "#6C63FF") for t in topics]
            fig2 = go.Figure(go.Bar(x=topics, y=scores, marker_color=colors))
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#A0A0CC"), yaxis=dict(range=[0,105]),
                margin=dict(l=0, r=0, t=10, b=0), height=300,
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 60px; color: #5050AA;">
                <div style="font-size: 48px;">🎯</div>
                <div style="margin-top: 12px;">Complete quizzes in multiple subjects to see your radar chart!</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_table, col_bar = st.columns([2, 3])

    with col_table:
        st.markdown("### 📋 Subject Summary")
        if performance:
            TOPIC_EMOJIS = {"Mathematics": "📐", "Physics": "⚛️", "Computer Science": "💻", "Chemistry": "🧪", "Biology": "🧬"}
            for p in performance:
                score = p["proficiency_score"]
                color = "#FF6B6B" if score < 40 else "#FFD93D" if score < 70 else "#6BCB77"
                level = "Beginner" if score < 40 else "Intermediate" if score < 70 else "Advanced"
                emoji = TOPIC_EMOJIS.get(p["topic"], "📚")
                st.markdown(f"""
                <div class="glass-card" style="padding: 16px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 600; color: #E0E0FF; font-size: 14px;">{emoji} {p['topic']}</div>
                            <div style="font-size: 12px; color: {color};">{level} · {p['attempts']} attempts</div>
                        </div>
                        <div style="font-size: 22px; font-weight: 800; color: {color};">{score:.0f}%</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); border-radius: 4px; height: 6px; margin-top: 10px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, {color}, {color}88); 
                            width: {score}%; height: 100%; border-radius: 4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No quiz data yet! Take a quiz to populate your dashboard.")

    with col_bar:
        st.markdown("### 🎯 Latest Quiz Scores by Topic")
        if quiz_history:
            # Get latest score per topic
            latest = {}
            for s in sorted(quiz_history, key=lambda x: x.get("session_date") or ""):
                latest[s["topic"]] = s["score"]
            
            topics = list(latest.keys())
            scores = list(latest.values())
            colors = [TOPIC_COLORS.get(t, "#6C63FF") for t in topics]
            
            fig3 = go.Figure(go.Bar(
                x=topics, y=scores,
                marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.1)", width=1)),
                text=[f"{s:.0f}%" for s in scores],
                textposition="outside",
                textfont=dict(color="#A0A0CC", size=13),
            ))
            # Add target line
            fig3.add_hline(y=70, line_dash="dash", line_color="rgba(255,217,61,0.6)",
                          annotation_text="Target 70%", annotation_font_color="#FFD93D")
            fig3.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#A0A0CC"),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", range=[0, 115]),
                margin=dict(l=0, r=0, t=10, b=40), height=300,
                showlegend=False,
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 60px; color: #5050AA;">
                <div style="font-size: 48px;">🗓️</div>
                <div style="margin-top: 12px;">Your performance chart will appear here!</div>
            </div>
            """, unsafe_allow_html=True)

    # Quick start
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ⚡ Quick Start")
    qa_cols = st.columns(5)
    topics_info = [
        ("📐", "Mathematics", "#6C63FF"),
        ("⚛️", "Physics", "#FF6B6B"),
        ("💻", "Computer Science", "#6BCB77"),
        ("🧪", "Chemistry", "#FFD93D"),
        ("🧬", "Biology", "#FF8B94"),
    ]
    for i, (emoji, topic, color) in enumerate(topics_info):
        with qa_cols[i]:
            if st.button(f"{emoji} {topic}", key=f"quick_{topic}", use_container_width=True):
                st.session_state.quiz_topic = topic
                st.session_state.current_page = "📝 Take Quiz"
                st.rerun()
