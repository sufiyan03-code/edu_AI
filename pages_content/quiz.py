"""
Quiz Page — Adaptive quiz engine with NLP analysis
"""
import streamlit as st
import time
import random
from datetime import datetime

from modules.quiz_engine import get_questions_for_topic, get_all_topics
from modules.nlp_analyzer import analyze_answer_quality, analyze_sentiment
from modules.recommender import get_adaptive_difficulty
from utils.db import (save_quiz_session, save_quiz_answer,
                      update_topic_performance, get_user_performance, update_streak)


def show_quiz():
    user = st.session_state.user

    st.markdown("""
    <h1 style="background: linear-gradient(135deg, #6C63FF, #C0C0FF); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        font-family: 'Space Grotesk', sans-serif; margin-bottom: 8px;">
        📝 Adaptive Quiz
    </h1>
    <p style="color: #7070AA; margin-bottom: 24px;">
        Questions adapt to your performance level in real-time
    </p>
    """, unsafe_allow_html=True)

    # If no quiz in progress — topic selection
    if not st.session_state.quiz_state or st.session_state.quiz_state.get("completed"):
        _show_topic_selection(user)
    else:
        _show_quiz_in_progress(user)


def _show_topic_selection(user):
    all_topics = get_all_topics()
    performance = get_user_performance(user["id"])

    # Pre-select topic if coming from dashboard
    default_topic = st.session_state.get("quiz_topic", all_topics[0])
    if default_topic not in all_topics:
        default_topic = all_topics[0]

    col_sel, col_info = st.columns([2, 3])

    with col_sel:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #E0E0FF; margin-top: 0;">⚙️ Quiz Settings</h3>
        </div>
        """, unsafe_allow_html=True)
        
        topic = st.selectbox(
            "📚 Select Subject",
            all_topics,
            index=all_topics.index(default_topic),
            key="topic_selector"
        )
        
        num_questions = st.slider("Number of Questions", min_value=5, max_value=12, value=8, step=1)
        
        # Show adaptive difficulty info
        rec_diff = get_adaptive_difficulty(topic, performance)
        diff_labels = {1: "🌱 Beginner", 2: "📘 Easy", 3: "⚡ Medium", 4: "🔥 Hard", 5: "💀 Expert"}
        diff_colors = {1: "#6BCB77", 2: "#9C92FF", 3: "#FFD93D", 4: "#FF8B94", 5: "#FF6B6B"}
        
        st.markdown(f"""
        <div style="background: rgba(108,99,255,0.1); border: 1px solid rgba(108,99,255,0.3); 
            border-radius: 10px; padding: 14px; margin: 12px 0;">
            <div style="font-size: 13px; color: #7070AA;">Adaptive Difficulty</div>
            <div style="font-size: 18px; font-weight: 700; color: {diff_colors[rec_diff]};">
                {diff_labels[rec_diff]}
            </div>
            <div style="font-size: 12px; color: #5050AA; margin-top: 4px;">
                Based on your {topic} performance
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Quiz!", use_container_width=True, key="start_quiz_btn"):
            questions = get_questions_for_topic(topic, n=num_questions, difficulty_target=rec_diff)
            random.shuffle(questions)
            st.session_state.quiz_state = {
                "topic": topic,
                "questions": questions,
                "current_idx": 0,
                "answers": [],
                "start_time": time.time(),
                "completed": False,
                "session_answers": [],
            }
            st.session_state.quiz_topic = topic
            st.rerun()

    with col_info:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #E0E0FF; margin-top: 0;">📊 Your Topic Performance</h3>
        </div>
        """, unsafe_allow_html=True)

        if performance:
            for p in performance:
                score = p["proficiency_score"]
                color = "#FF6B6B" if score < 40 else "#FFD93D" if score < 70 else "#6BCB77"
                level = "Beginner" if score < 40 else "Intermediate" if score < 70 else "Advanced"
                topic_emojis = {"Mathematics": "📐", "Physics": "⚛️", "Computer Science": "💻", "Chemistry": "🧪", "Biology": "🧬"}
                e = topic_emojis.get(p['topic'], '📚')
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 12px; padding: 10px; 
                    margin: 4px 0; border-radius: 8px; background: rgba(255,255,255,0.03);">
                    <span style="font-size: 20px;">{e}</span>
                    <div style="flex: 1;">
                        <div style="font-size: 14px; color: #E0E0FF; font-weight: 500;">{p['topic']}</div>
                        <div style="background: rgba(255,255,255,0.05); border-radius: 4px; height: 5px; margin-top: 6px;">
                            <div style="background: linear-gradient(90deg, {color}, {color}88); 
                                width: {score}%; height: 100%; border-radius: 4px;"></div>
                        </div>
                    </div>
                    <div style="font-weight: 700; color: {color}; font-size: 16px;">{score:.0f}%</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No previous data — all topics start at beginner level!")

        # How it works
        st.markdown("""
        <div style="background: rgba(108,99,255,0.05); border: 1px solid rgba(108,99,255,0.2); 
            border-radius: 10px; padding: 16px; margin-top: 16px;">
            <div style="font-weight: 600; color: #9C92FF; margin-bottom: 8px;">🧠 How Adaptive Learning Works</div>
            <div style="font-size: 13px; color: #7070AA; line-height: 1.8;">
                • Questions difficulty adjusts to your score<br>
                • NLP analyzes your explanations<br>
                • Topic mastery updates live<br>
                • Recommendations improve after each quiz
            </div>
        </div>
        """, unsafe_allow_html=True)


def _show_quiz_in_progress(user):
    state = st.session_state.quiz_state
    questions = state["questions"]
    idx = state["current_idx"]

    if idx >= len(questions):
        _show_quiz_results(user, state)
        return

    q = questions[idx]
    total = len(questions)

    # Progress header
    progress_pct = idx / total
    elapsed = int(time.time() - state["start_time"])
    mins, secs = divmod(elapsed, 60)

    col_p, col_t = st.columns([3, 1])
    with col_p:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
            <div style="font-size: 14px; color: #7070AA;">Question {idx+1} of {total}</div>
            <div style="flex: 1; background: rgba(255,255,255,0.05); border-radius: 4px; height: 8px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #6C63FF, #9C92FF); 
                    width: {progress_pct*100:.0f}%; height: 100%; border-radius: 4px; 
                    transition: width 0.5s ease;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_t:
        st.markdown(f"""
        <div style="text-align: right; color: #6C63FF; font-weight: 600; font-size: 16px;">
            ⏱️ {mins:02d}:{secs:02d}
        </div>
        """, unsafe_allow_html=True)

    # Difficulty badge
    diff_map = {1: ("🌱 Beginner", "#6BCB77"), 2: ("📘 Easy", "#9C92FF"),
                3: ("⚡ Medium", "#FFD93D"), 4: ("🔥 Hard", "#FF8B94"), 5: ("💀 Expert", "#FF6B6B")}
    diff_label, diff_color = diff_map.get(q["difficulty"], ("⚡ Medium", "#FFD93D"))

    st.markdown(f"""
    <div class="glass-card" style="margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
            <span style="font-size: 12px; color: #7070AA; background: rgba(255,255,255,0.05); 
                padding: 4px 10px; border-radius: 20px;">{q['subtopic']}</span>
            <span style="font-size: 12px; color: {diff_color}; background: rgba(255,255,255,0.05); 
                padding: 4px 10px; border-radius: 20px;">{diff_label}</span>
        </div>
        <h2 style="color: #E0E0FF; font-size: 20px; margin: 0; line-height: 1.5; font-family: 'Inter', sans-serif;">
            {q['question']}
        </h2>
    </div>
    """, unsafe_allow_html=True)

    feedback = state.get("current_feedback")
    if feedback:
        # Show Feedback phase
        is_correct = feedback["is_correct"]
        if is_correct:
            st.markdown(f"""
            <div class="correct-answer" style="margin-top: 12px;">
                <strong>✅ Correct!</strong> {q['explanation']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="wrong-answer" style="margin-top: 12px;">
                <strong>❌ Wrong.</strong> Correct: <strong>{q['correct']}</strong><br>
                {q['explanation']}
            </div>
            """, unsafe_allow_html=True)

        if feedback.get("response_text") and feedback.get("nlp_result"):
            nlp_res = feedback["nlp_result"]
            sentiment_emoji = "😐" if nlp_res.get("sentiment", {}).get("label") == "Neutral" else "😊" if nlp_res.get("sentiment", {}).get("label") == "Confident" else "😟"
            st.markdown(f"""
            <div style="background: rgba(108,99,255,0.08); border: 1px solid rgba(108,99,255,0.2); 
                border-radius: 10px; padding: 12px; margin-top: 12px;">
                <div style="font-size: 13px; color: #9C92FF; font-weight: 600;">🧠 NLP Insight</div>
                <div style="font-size: 13px; color: #A0A0CC; margin-top: 4px;">
                    {sentiment_emoji} Mood: <strong>{nlp_res.get("sentiment", {}).get("label", "Neutral")}</strong> · 
                    {nlp_res.get("feedback", "")}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        btn_label = "Next Question →" if idx + 1 < total else "View Quiz Results →"
        if st.button(btn_label, key=f"next_{idx}", use_container_width=True):
            state["current_feedback"] = None
            state["current_idx"] += 1
            if state["current_idx"] >= len(questions):
                _save_quiz_results(user, state)
                state["completed"] = True
            st.rerun()
    else:
        # Answer options
        selected_answer = st.radio(
            "Choose your answer:",
            q["options"],
            key=f"answer_{idx}",
            label_visibility="collapsed"
        )

        # Optional explanation text
        st.markdown("**✍️ Explain your thinking** *(optional — helps NLP analyze your understanding)*")
        response_text = st.text_area(
            "Your explanation",
            placeholder="E.g. 'I think this is correct because...' or 'I'm not sure, but...'",
            key=f"response_{idx}",
            label_visibility="collapsed",
            height=80
        )

        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn1:
            if st.button("✅ Submit Answer", key=f"submit_{idx}", use_container_width=True):
                is_correct = selected_answer == q["correct"]

                # NLP Analysis
                nlp_result = analyze_answer_quality(
                    response_text, q["correct"], q["topic"]
                ) if response_text else {"sentiment": {"score": 0, "label": "Neutral"}, "quality_score": 0, "feedback": ""}
                
                sentiment_score = nlp_result["sentiment"]["score"]

                ans_obj = {
                    "question": q["question"],
                    "question_id": q.get("id", "Q"),
                    "user_answer": selected_answer,
                    "correct_answer": q["correct"],
                    "is_correct": is_correct,
                    "explanation": q["explanation"],
                    "topic": q["topic"],
                    "subtopic": q["subtopic"],
                    "response_text": response_text,
                    "nlp_result": nlp_result,
                    "sentiment_score": sentiment_score,
                }

                # Store answer
                state["session_answers"].append(ans_obj)
                state["current_feedback"] = ans_obj
                st.rerun()

        with col_btn2:
            # Skip button
            if st.button("⏭ Skip Question", key=f"skip_{idx}"):
                ans_obj = {
                    "question": q["question"],
                    "question_id": q.get("id", "Q"),
                    "user_answer": "Skipped",
                    "correct_answer": q["correct"],
                    "is_correct": False,
                    "explanation": q["explanation"],
                    "topic": q["topic"],
                    "subtopic": q["subtopic"],
                    "response_text": "",
                    "nlp_result": {},
                    "sentiment_score": 0,
                }
                state["session_answers"].append(ans_obj)
                state["current_feedback"] = ans_obj
                st.rerun()


def _save_quiz_results(user, state):
    answers = state["session_answers"]
    topic = state["topic"]
    correct_count = sum(1 for a in answers if a["is_correct"])
    total = len(answers)
    score = (correct_count / total * 100) if total > 0 else 0
    time_taken = int(time.time() - state["start_time"])

    # Determine difficulty label
    diff_score = score
    difficulty = "easy" if diff_score < 40 else "medium" if diff_score < 70 else "hard"

    session_id = save_quiz_session(user["id"], topic, score, total, correct_count, time_taken, difficulty)
    update_topic_performance(user["id"], topic, score)
    update_streak(user["id"])

    for a in answers:
        save_quiz_answer(
            session_id, user["id"], topic, a.get("question_id", "Q"),
            a["question"], a["user_answer"], a["correct_answer"],
            a["is_correct"], a["response_text"],
            a["sentiment_score"], 0
        )


def _show_quiz_results(user, state):
    answers = state["session_answers"]
    correct = sum(1 for a in answers if a["is_correct"])
    total = len(answers)
    score = (correct / total * 100) if total > 0 else 0
    time_taken = int(time.time() - state["start_time"])
    mins, secs = divmod(time_taken, 60)

    # Score color
    color = "#FF6B6B" if score < 40 else "#FFD93D" if score < 70 else "#6BCB77"
    grade = "F" if score < 40 else "C" if score < 55 else "B" if score < 70 else "A" if score < 90 else "A+"
    message = "Keep practicing! 💪" if score < 50 else "Good job! 👍" if score < 75 else "Excellent! 🌟"

    st.markdown(f"""
    <div class="hero-banner" style="margin-bottom: 32px;">
        <div style="font-size: 72px; line-height: 1;">{grade}</div>
        <h2 style="color: {color}; font-size: 36px; margin: 8px 0; font-family: 'Space Grotesk', sans-serif;">
            {score:.1f}%
        </h2>
        <p style="color: #A0A0CC; font-size: 18px;">{message}</p>
        <div style="display: flex; justify-content: center; gap: 32px; margin-top: 16px;">
            <div style="text-align: center;">
                <div style="font-size: 24px; font-weight: 700; color: #6BCB77;">✅ {correct}</div>
                <div style="font-size: 12px; color: #7070AA;">Correct</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 24px; font-weight: 700; color: #FF6B6B;">❌ {total-correct}</div>
                <div style="font-size: 12px; color: #7070AA;">Wrong</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 24px; font-weight: 700; color: #9C92FF;">⏱️ {mins}:{secs:02d}</div>
                <div style="font-size: 12px; color: #7070AA;">Time Taken</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Take Another Quiz", use_container_width=True):
            st.session_state.quiz_state = None
            st.rerun()
    with col2:
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.current_page = "📊 Analytics"
            st.rerun()

    # Answer Review
    st.markdown("### 📋 Answer Review")
    for i, a in enumerate(answers):
        is_correct = a["is_correct"]
        bg = "rgba(107,203,119,0.08)" if is_correct else "rgba(255,107,107,0.08)"
        border = "rgba(107,203,119,0.3)" if is_correct else "rgba(255,107,107,0.3)"
        icon = "✅" if is_correct else "❌"
        
        with st.expander(f"{icon} Q{i+1}: {a['question'][:70]}...", expanded=False):
            st.markdown(f"""
            <div style="background: {bg}; border: 1px solid {border}; border-radius: 10px; padding: 16px;">
                <div><strong style="color: #A0A0CC;">Your Answer:</strong> 
                    <span style="color: {'#6BCB77' if is_correct else '#FF6B6B'};">{a['user_answer']}</span>
                </div>
                <div style="margin-top: 8px;"><strong style="color: #A0A0CC;">Correct Answer:</strong> 
                    <span style="color: #6BCB77;">{a['correct_answer']}</span>
                </div>
                <div style="margin-top: 8px; color: #9C92FF; font-size: 13px;">
                    💡 {a['explanation']}
                </div>
                {"<div style='margin-top: 8px; background: rgba(108,99,255,0.1); border-radius: 8px; padding: 10px;'><span style='font-size: 12px; color: #7070AA;'>🧠 Your explanation: </span><span style='color: #A0A0CC; font-size: 13px;'>" + a.get('response_text','') + "</span></div>" if a.get('response_text') else ""}
            </div>
            """, unsafe_allow_html=True)
