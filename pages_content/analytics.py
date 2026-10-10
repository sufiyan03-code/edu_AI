"""
Analytics Page — Deep performance analysis with NLP insights (pandas-free)
"""
import streamlit as st
import plotly.graph_objects as go
from collections import defaultdict

from utils.db import get_user_performance, get_quiz_history, get_answer_history
from modules.nlp_analyzer import generate_nlp_insights, extract_keywords

TOPIC_COLORS = {
    "Mathematics": "#6C63FF", "Physics": "#FF6B6B",
    "Computer Science": "#6BCB77", "Chemistry": "#FFD93D", "Biology": "#FF8B94"
}
TOPIC_EMOJIS = {"Mathematics": "📐", "Physics": "⚛️", "Computer Science": "💻", "Chemistry": "🧪", "Biology": "🧬"}


def show_analytics():
    user = st.session_state.user

    st.markdown("""
    <h1 style="background: linear-gradient(135deg, #6C63FF, #C0C0FF); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        font-family: 'Space Grotesk', sans-serif; margin-bottom: 8px;">
        📊 Learning Analytics
    </h1>
    <p style="color: #7070AA; margin-bottom: 24px;">
        Deep insights into your learning patterns powered by NLP
    </p>
    """, unsafe_allow_html=True)

    performance = get_user_performance(user["id"])
    quiz_history = get_quiz_history(user["id"])
    answer_history = get_answer_history(user["id"])

    if not quiz_history:
        st.markdown("""
        <div style="text-align: center; padding: 80px 20px;">
            <div style="font-size: 64px;">📊</div>
            <h2 style="color: #5050AA; margin: 16px 0;">No Data Yet</h2>
            <p style="color: #404060;">Complete at least one quiz to see your analytics!</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📝 Take a Quiz Now"):
            st.session_state.current_page = "📝 Take Quiz"
            st.rerun()
        return

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Performance", "🧠 NLP Insights", "📋 Topic Breakdown", "📅 History"])

    # ── TAB 1: Performance ──
    with tab1:
        sorted_history = sorted(quiz_history, key=lambda x: x.get("session_date") or "")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📈 Score Over Time (All Topics)")
            topic_sessions = defaultdict(lambda: {"dates": [], "scores": []})
            for s in sorted_history:
                topic_sessions[s["topic"]]["dates"].append((s.get("session_date") or "")[:16])
                topic_sessions[s["topic"]]["scores"].append(s["score"])

            fig = go.Figure()
            for topic, data in topic_sessions.items():
                color = TOPIC_COLORS.get(topic, "#6C63FF")
                fig.add_trace(go.Scatter(
                    x=data["dates"], y=data["scores"],
                    mode="lines+markers", name=topic,
                    marker=dict(size=7, color=color), line=dict(color=color, width=2),
                ))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#A0A0CC"),
                xaxis=dict(showgrid=False), yaxis=dict(gridcolor="rgba(255,255,255,0.05)", range=[0, 105]),
                legend=dict(bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=0, r=0, t=10, b=0), height=280,
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### 🎯 Proficiency by Topic")
            if performance:
                topics = [p["topic"] for p in performance]
                scores = [p["proficiency_score"] for p in performance]
                colors = [TOPIC_COLORS.get(t, "#6C63FF") for t in topics]
                fig2 = go.Figure(go.Bar(
                    x=scores, y=topics, orientation='h',
                    marker=dict(color=colors, line=dict(width=0)),
                    text=[f"{s:.0f}%" for s in scores],
                    textposition='inside', textfont=dict(color="white", size=13),
                ))
                fig2.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#A0A0CC"),
                    xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", range=[0, 105]),
                    yaxis=dict(showgrid=False),
                    margin=dict(l=0, r=0, t=10, b=0), height=280,
                )
                st.plotly_chart(fig2, use_container_width=True)

        # Time taken distribution
        st.markdown("#### ⏱️ Time Per Quiz Session (minutes)")
        topic_times = defaultdict(list)
        for s in sorted_history:
            if s.get("time_taken"):
                topic_times[s["topic"]].append(s["time_taken"] / 60)

        if topic_times:
            fig3 = go.Figure()
            for topic, times in topic_times.items():
                fig3.add_trace(go.Box(
                    y=times, name=topic,
                    marker_color=TOPIC_COLORS.get(topic, "#6C63FF"),
                    line_color=TOPIC_COLORS.get(topic, "#6C63FF"),
                ))
            fig3.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#A0A0CC"),
                yaxis=dict(title="Minutes", gridcolor="rgba(255,255,255,0.05)"),
                xaxis=dict(showgrid=False),
                margin=dict(l=0, r=0, t=10, b=0), height=260, showlegend=False,
            )
            st.plotly_chart(fig3, use_container_width=True)

    # ── TAB 2: NLP Insights ──
    with tab2:
        st.markdown("### 🧠 NLP Analysis of Your Responses")
        answers_with_text = [a for a in answer_history if a.get("response_text", "").strip()]

        if not answers_with_text:
            st.info("💡 Write explanations during quizzes to unlock NLP insights! These show your understanding patterns.")
            st.markdown("""
            <div style="background: rgba(108,99,255,0.08); border: 1px solid rgba(108,99,255,0.2); 
                border-radius: 12px; padding: 20px; margin-top: 16px;">
                <div style="font-weight: 600; color: #9C92FF; margin-bottom: 8px;">How to unlock NLP insights:</div>
                <div style="color: #A0A0CC; font-size: 14px; line-height: 1.8;">
                    1. Go to <strong>Take Quiz</strong><br>
                    2. After choosing an answer, write your reasoning in the explanation box<br>
                    3. The AI will analyze your confidence, keywords, and understanding!
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            insights = generate_nlp_insights(answer_history)

            col_mood, col_words = st.columns([1, 2])
            with col_mood:
                sentiment_score = insights.get("overall_sentiment", 0)
                mood = insights.get("overall_mood", "Neutral")
                mood_emoji = "😊" if mood == "Confident" else "😟" if mood == "Struggling" else "😐"
                mood_color = "#6BCB77" if mood == "Confident" else "#FF6B6B" if mood == "Struggling" else "#FFD93D"

                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=round((sentiment_score + 1) * 50, 1),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': f"{mood_emoji} Confidence Score", 'font': {'color': '#A0A0CC', 'size': 14}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickcolor': '#A0A0CC'},
                        'bar': {'color': mood_color},
                        'bgcolor': 'rgba(0,0,0,0)',
                        'steps': [
                            {'range': [0, 35], 'color': 'rgba(255,107,107,0.2)'},
                            {'range': [35, 65], 'color': 'rgba(255,217,61,0.2)'},
                            {'range': [65, 100], 'color': 'rgba(107,203,119,0.2)'},
                        ],
                    }
                ))
                fig_gauge.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#A0A0CC"),
                    height=250, margin=dict(l=20, r=20, t=40, b=0)
                )
                st.plotly_chart(fig_gauge, use_container_width=True)
                st.markdown(f"""
                <div style="text-align: center; margin-top: -10px;">
                    <div style="color: {mood_color}; font-weight: 700; font-size: 18px;">{mood}</div>
                    <div style="color: #7070AA; font-size: 13px;">{insights.get('total_responses', 0)} responses analyzed</div>
                </div>
                """, unsafe_allow_html=True)

            with col_words:
                st.markdown("#### 🔑 Top Keywords in Your Responses")
                top_kw = insights.get("top_keywords", [])
                if top_kw:
                    words = [k["word"] for k in top_kw]
                    scores_kw = [k["score"] for k in top_kw]
                    fig_kw = go.Figure(go.Bar(
                        x=scores_kw, y=words, orientation="h",
                        marker=dict(color=scores_kw, colorscale=[[0, "#3D3A8A"], [1, "#9C92FF"]]),
                    ))
                    fig_kw.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#A0A0CC"),
                        margin=dict(l=0, r=0, t=0, b=0), height=250,
                        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
                        yaxis=dict(showgrid=False),
                    )
                    st.plotly_chart(fig_kw, use_container_width=True)

            # Strength vs confusion keywords
            col_strong, col_confused = st.columns(2)
            with col_strong:
                st.markdown("#### 💪 Keywords (Correct Answers)")
                strong_kw = insights.get("strong_keywords", [])
                if strong_kw:
                    for kw in strong_kw[:6]:
                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; align-items: center;
                            padding: 6px 12px; margin: 4px 0; border-radius: 8px;
                            background: rgba(107,203,119,0.1); border: 1px solid rgba(107,203,119,0.2);">
                            <span style="color: #6BCB77; font-size: 14px;">✅ {kw['word']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Write explanations on correct answers to see this!")

            with col_confused:
                st.markdown("#### 🤔 Keywords (Wrong Answers)")
                confused_kw = insights.get("confused_keywords", [])
                if confused_kw:
                    for kw in confused_kw[:6]:
                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; align-items: center;
                            padding: 6px 12px; margin: 4px 0; border-radius: 8px;
                            background: rgba(255,107,107,0.1); border: 1px solid rgba(255,107,107,0.2);">
                            <span style="color: #FF6B6B; font-size: 14px;">❌ {kw['word']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No wrong-answer explanations yet.")

    # ── TAB 3: Topic Breakdown ──
    with tab3:
        st.markdown("### 📋 Detailed Topic Analysis")
        if performance:
            for p in performance:
                topic = p["topic"]
                score = p["proficiency_score"]
                color = "#FF6B6B" if score < 40 else "#FFD93D" if score < 70 else "#6BCB77"
                level = "Beginner" if score < 40 else "Intermediate" if score < 70 else "Advanced"
                emoji = TOPIC_EMOJIS.get(topic, "📚")

                with st.expander(f"{emoji} {topic} — {score:.0f}% ({level})", expanded=False):
                    topic_answers = [a for a in answer_history if a.get("topic") == topic]
                    total_a = len(topic_answers)
                    correct_a = sum(1 for a in topic_answers if a.get("is_correct"))
                    wrong_a = total_a - correct_a

                    c1, c2, c3 = st.columns(3)
                    c1.metric("Total Answers", total_a)
                    c2.metric("Correct", correct_a, delta=f"{correct_a/total_a*100:.0f}%" if total_a > 0 else "0%")
                    c3.metric("Wrong", wrong_a)

                    if total_a > 0:
                        fig_d = go.Figure(go.Pie(
                            values=[max(correct_a, 0.01), max(wrong_a, 0.01)],
                            labels=["Correct", "Wrong"],
                            hole=0.65,
                            marker=dict(colors=["#6BCB77", "#FF6B6B"]),
                            textinfo="percent",
                        ))
                        fig_d.update_layout(
                            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#A0A0CC"), showlegend=True,
                            legend=dict(bgcolor="rgba(0,0,0,0)"),
                            margin=dict(l=0, r=0, t=0, b=0), height=180,
                        )
                        st.plotly_chart(fig_d, use_container_width=True)

    # ── TAB 4: History ──
    with tab4:
        st.markdown("### 📅 Quiz Session History")
        if quiz_history:
            for s in sorted(quiz_history, key=lambda x: x.get("session_date") or "", reverse=True):
                score = s.get("score", 0)
                score_color = "#FF6B6B" if score < 40 else "#FFD93D" if score < 70 else "#6BCB77"
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 16px; padding: 12px 16px; 
                    margin: 6px 0; border-radius: 10px; background: rgba(255,255,255,0.03);
                    border: 1px solid rgba(255,255,255,0.07);">
                    <div style="font-size: 22px;">{TOPIC_EMOJIS.get(s['topic'],'📚')}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #E0E0FF; font-size: 14px;">{s['topic']}</div>
                        <div style="font-size: 12px; color: #7070AA;">
                            {(s.get('session_date') or '')[:16]} · {s.get('correct_answers',0)}/{s.get('total_questions',0)} correct · {s.get('difficulty','').title()}
                        </div>
                    </div>
                    <div style="font-size: 20px; font-weight: 800; color: {score_color};">{score:.0f}%</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No history yet!")
