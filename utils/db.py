"""
Database utility module — SQLite with SQLAlchemy
Handles all persistent storage for the adaptive learning system.
"""
import sqlite3
import json
import hashlib
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "learning.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize all tables."""
    conn = get_conn()
    c = conn.cursor()
    
    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            email TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            avatar_color TEXT DEFAULT '#6C63FF'
        )
    """)
    
    # Quiz sessions
    c.execute("""
        CREATE TABLE IF NOT EXISTS quiz_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            score REAL,
            total_questions INTEGER,
            correct_answers INTEGER,
            time_taken INTEGER,
            difficulty TEXT,
            session_date TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Individual answers
    c.execute("""
        CREATE TABLE IF NOT EXISTS quiz_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            user_id INTEGER,
            topic TEXT,
            question_id TEXT,
            question_text TEXT,
            user_answer TEXT,
            correct_answer TEXT,
            is_correct INTEGER,
            response_text TEXT,
            sentiment_score REAL,
            confidence_score REAL,
            answered_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (session_id) REFERENCES quiz_sessions(id)
        )
    """)
    
    # Topic performance summary
    c.execute("""
        CREATE TABLE IF NOT EXISTS topic_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            topic TEXT,
            proficiency_score REAL DEFAULT 0,
            attempts INTEGER DEFAULT 0,
            last_updated TEXT DEFAULT (datetime('now')),
            UNIQUE(user_id, topic),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Chat history
    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,
            message TEXT,
            timestamp TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Study streaks
    c.execute("""
        CREATE TABLE IF NOT EXISTS study_streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            current_streak INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            last_study_date TEXT,
            total_study_days INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, full_name, email):
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (username, password_hash, full_name, email) VALUES (?, ?, ?, ?)",
            (username, hash_password(password), full_name, email)
        )
        conn.commit()
        user_id = c.lastrowid
        # Init streak
        c.execute("INSERT INTO study_streaks (user_id) VALUES (?)", (user_id,))
        conn.commit()
        return True, user_id
    except sqlite3.IntegrityError:
        return False, None
    finally:
        conn.close()

def login_user(username, password):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM users WHERE username=? AND password_hash=?",
        (username, hash_password(password))
    )
    row = c.fetchone()
    conn.close()
    if row:
        return True, dict(row)
    return False, None

def save_quiz_session(user_id, topic, score, total_q, correct, time_taken, difficulty):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO quiz_sessions (user_id, topic, score, total_questions, correct_answers, time_taken, difficulty)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, topic, score, total_q, correct, time_taken, difficulty))
    session_id = c.lastrowid
    conn.commit()
    conn.close()
    return session_id

def save_quiz_answer(session_id, user_id, topic, q_id, q_text, user_ans, correct_ans, is_correct, response_text="", sentiment=0.0, confidence=0.0):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO quiz_answers 
        (session_id, user_id, topic, question_id, question_text, user_answer, correct_answer, is_correct, response_text, sentiment_score, confidence_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (session_id, user_id, topic, q_id, q_text, user_ans, correct_ans, int(is_correct), response_text, sentiment, confidence))
    conn.commit()
    conn.close()

def update_topic_performance(user_id, topic, score):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO topic_performance (user_id, topic, proficiency_score, attempts)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(user_id, topic) DO UPDATE SET
            proficiency_score = (proficiency_score * attempts + ?) / (attempts + 1),
            attempts = attempts + 1,
            last_updated = datetime('now')
    """, (user_id, topic, score, score))
    conn.commit()
    conn.close()

def get_user_performance(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT topic, proficiency_score, attempts, last_updated 
        FROM topic_performance WHERE user_id=? ORDER BY topic
    """, (user_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_quiz_history(user_id, limit=50):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM quiz_sessions WHERE user_id=? 
        ORDER BY session_date DESC LIMIT ?
    """, (user_id, limit))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_answer_history(user_id, limit=100):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM quiz_answers WHERE user_id=? 
        ORDER BY answered_at DESC LIMIT ?
    """, (user_id, limit))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def save_chat_message(user_id, role, message):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO chat_history (user_id, role, message) VALUES (?, ?, ?)",
        (user_id, role, message)
    )
    conn.commit()
    conn.close()

def get_chat_history(user_id, limit=50):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT role, message, timestamp FROM chat_history 
        WHERE user_id=? ORDER BY id DESC LIMIT ?
    """, (user_id, limit))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return list(reversed(rows))

def update_streak(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM study_streaks WHERE user_id=?", (user_id,))
    row = c.fetchone()
    if row:
        row = dict(row)
        last = row.get("last_study_date", "")
        from datetime import timedelta
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        if last == today:
            conn.close()
            return
        elif last == yesterday:
            new_streak = row["current_streak"] + 1
        else:
            new_streak = 1
        longest = max(row["longest_streak"], new_streak)
        c.execute("""
            UPDATE study_streaks SET current_streak=?, longest_streak=?, 
            last_study_date=?, total_study_days=total_study_days+1 
            WHERE user_id=?
        """, (new_streak, longest, today, user_id))
    else:
        c.execute("""
            INSERT INTO study_streaks (user_id, current_streak, longest_streak, last_study_date, total_study_days)
            VALUES (?, 1, 1, ?, 1)
        """, (user_id, today))
    conn.commit()
    conn.close()

def get_streak(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM study_streaks WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else {"current_streak": 0, "longest_streak": 0, "total_study_days": 0}

def get_all_usernames():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT username FROM users")
    rows = [r[0] for r in c.fetchall()]
    conn.close()
    return rows
