"""
Leaderboard Page
"""
import streamlit as st
import plotly.graph_objects as go

from utils.db import get_conn


def get_leaderboard_data():
    """Fetch leaderboard — top students by avg proficiency score."""
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT u.username, u.full_name, u.avatar_color,
               COALESCE(AVG(tp.proficiency_score), 0) as avg_score,
               COUNT(DISTINCT tp.topic) as topics_mastered,
               COALESCE(SUM(tp.attempts), 0) as total_attempts,
               COALESCE(ss.current_streak, 0) as streak,
               COALESCE(ss.total_study_days, 0) as study_days
        FROM users u
        JOIN topic_performance tp ON u.id = tp.user_id
        LEFT JOIN study_streaks ss ON u.id = ss.user_id
        GROUP BY u.id, u.username, u.full_name, u.avatar_color, ss.current_streak, ss.total_study_days
        ORDER BY avg_score DESC
        LIMIT 20
    """)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def show_leaderboard():
    user = st.session_state.user

    st.markdown("""
    <h1 style="background: linear-gradient(135deg, #FFD93D, #FF8B94); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        font-family: 'Space Grotesk', sans-serif; margin-bottom: 8px;">
        🏆 Leaderboard
    </h1>
    <p style="color: #7070AA; margin-bottom: 24px;">
        Top learners ranked by overall performance score
    </p>
    """, unsafe_allow_html=True)

    data = get_leaderboard_data()

    if not data:
        st.markdown("""
        <div style="text-align: center; padding: 80px 20px;">
            <div style="font-size: 64px;">🏆</div>
            <h2 style="color: #5050AA;">No rankings yet!</h2>
            <p style="color: #404060;">Be the first to complete quizzes and claim the top spot!</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Podium for top 3
    if len(data) >= 3:
        st.markdown("### 🥇 Top 3 Learners")
        col2, col1, col3 = st.columns([1, 1.2, 1])

        podium_data = [(col1, data[0], "🥇", "#FFD700", 1),
                       (col2, data[1], "🥈", "#C0C0C0", 2),
                       (col3, data[2], "🥉", "#CD7F32", 3)]

        for col, d, trophy, color, rank in podium_data:
            with col:
                initials = "".join(n[0].upper() for n in d["full_name"].split()[:2])
                height = "120px" if rank == 1 else "90px"
                st.markdown(f"""
                <div style="text-align: center; padding: 20px 10px;">
                    <div style="font-size: 36px; margin-bottom: 8px;">{trophy}</div>
                    <div style="width: 60px; height: 60px; border-radius: 50%; 
                        background: linear-gradient(135deg, {color}, {color}88);
                        display: flex; align-items: center; justify-content: center;
                        margin: 0 auto 10px; font-size: 20px; font-weight: 700; color: #0D0D1A;
                        box-shadow: 0 4px 20px {color}66;">
                        {initials}
                    </div>
                    <div style="font-weight: 700; color: #E0E0FF; font-size: 14px;">{d['full_name']}</div>
                    <div style="color: {color}; font-size: 22px; font-weight: 800; margin-top: 6px;">
                        {d['avg_score']:.1f}%
                    </div>
                    <div style="color: #7070AA; font-size: 12px;">🔥 {d['streak']} day streak</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Full table
    st.markdown("### 📊 Full Rankings")

    medal_map = {1: "🥇", 2: "🥈", 3: "🥉"}

    for i, d in enumerate(data, 1):
        is_current = d["username"] == user["username"]
        bg = "rgba(108,99,255,0.15)" if is_current else "rgba(255,255,255,0.03)"
        border = "rgba(108,99,255,0.5)" if is_current else "rgba(255,255,255,0.07)"
        rank_label = medal_map.get(i, f"#{i}")
        initials = "".join(n[0].upper() for n in d["full_name"].split()[:2])
        
        score_color = "#FF6B6B" if d["avg_score"] < 40 else "#FFD93D" if d["avg_score"] < 70 else "#6BCB77"

        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 16px; padding: 14px 18px; margin: 6px 0;
            border-radius: 12px; background: {bg}; border: 1px solid {border};
            transition: all 0.2s ease;">
            <div style="font-size: 18px; width: 36px; text-align: center; font-weight: 700;">{rank_label}</div>
            <div style="width: 42px; height: 42px; border-radius: 50%; background: linear-gradient(135deg, #6C63FF, #9C92FF);
                display: flex; align-items: center; justify-content: center; font-size: 16px; 
                font-weight: 700; color: white; flex-shrink: 0;">{initials}</div>
            <div style="flex: 1;">
                <div style="color: #E0E0FF; font-weight: 600; font-size: 14px;">
                    {d['full_name']} {'<span style="color:#6C63FF; font-size:12px;">(You)</span>' if is_current else ''}
                </div>
                <div style="color: #7070AA; font-size: 12px;">@{d['username']} · {d['topics_mastered']} topics · {d['total_attempts']} attempts</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 20px; font-weight: 800; color: {score_color};">{d['avg_score']:.1f}%</div>
                <div style="font-size: 12px; color: #FFD93D;">🔥 {d['streak']} streak</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Score distribution chart
    if len(data) >= 3:
        st.markdown("### 📈 Score Distribution")
        fig = go.Figure(go.Bar(
            x=[d["full_name"].split()[0] for d in data],
            y=[d["avg_score"] for d in data],
            marker=dict(
                color=[d["avg_score"] for d in data],
                colorscale=[[0, "#FF6B6B"], [0.5, "#FFD93D"], [1, "#6BCB77"]],
            ),
            text=[f"{d['avg_score']:.0f}%" for d in data],
            textposition="outside",
            textfont=dict(color="#A0A0CC"),
        ))
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#A0A0CC"),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", range=[0, 110]),
            margin=dict(l=0, r=0, t=10, b=0), height=300,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
