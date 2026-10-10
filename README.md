# 🎓 EduAI — AI Personalized Learning System

A complete, production-ready AI-based adaptive learning system built with Streamlit.

---

## 🚀 How to Run

```bash
cd d:\ML-CSE\adaptive_learning
streamlit run app.py
```

App will launch at: **http://localhost:8501**

**Demo credentials:** `demo` / `demo123`

---

## 📁 Project Structure

```
adaptive_learning/
├── app.py                        # Main entry point & routing
├── requirements.txt              # Dependencies
├── .streamlit/
│   └── config.toml              # Theme (dark purple)
├── data/
│   └── learning.db              # SQLite database (auto-created)
├── modules/
│   ├── quiz_engine.py           # 60+ question bank, adaptive difficulty
│   ├── nlp_analyzer.py          # Sentiment, keywords, similarity (no heavy deps)
│   ├── recommender.py           # Learning path & resource recommender
│   └── chatbot.py               # AI Tutor knowledge base
├── pages_content/
│   ├── dashboard.py             # Overview, charts, metrics
│   ├── quiz.py                  # Adaptive quiz engine
│   ├── analytics.py             # Deep analytics + NLP insights
│   ├── recommendations.py       # Personalized learning path
│   ├── chatbot_ui.py            # Chat interface
│   └── leaderboard.py           # Rankings
└── utils/
    └── db.py                    # SQLite database layer
```

---

## ✨ Features

| Feature | Details |
|---------|---------|
| 🔐 **Auth** | Register/Login with password hashing |
| 🏠 **Dashboard** | Score progression, radar chart, streaks, quick-start |
| 📝 **Adaptive Quiz** | 60+ questions across 5 subjects, IRT-based difficulty |
| 🧠 **NLP Analysis** | Sentiment, keywords, confidence from student explanations |
| 📊 **Analytics** | Plotly charts — trends, box plots, donut charts, gauges |
| 🎯 **Recommendations** | Learning path, resources by proficiency, priority topics |
| 🤖 **AI Tutor** | STEM knowledge base chatbot, quick topics, persistent history |
| 🏆 **Leaderboard** | Podium, rankings, streaks for all students |
| 🔥 **Streaks** | Daily study streak tracking |

---

## 🌐 Deploy to Streamlit Cloud (Free)

1. Push this folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file**: `adaptive_learning/app.py`
5. Click **Deploy** — live in 2 minutes!

---

## 🧠 ML/AI Techniques Used

- **Adaptive Difficulty** — IRT-based (Item Response Theory) question selection
- **NLP Sentiment Analysis** — Bag-of-words scoring on student explanations  
- **TF-IDF Keyword Extraction** — Identifies confused vs confident vocabulary
- **Answer Similarity** — Cosine similarity on tokenized text
- **Collaborative Filtering (light)** — Topic profile updates with weighted average
- **Learning Path Generation** — Status-based recommendation ordering

---

## 🎨 Design

- Dark mode with purple/violet gradient palette
- Google Fonts: Inter + Space Grotesk
- Glassmorphism cards with hover effects
- Plotly interactive charts: line, bar, radar, pie, gauge, box
- Responsive sidebar navigation with user profile
