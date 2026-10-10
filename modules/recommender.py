"""
Recommender Module
- Topic-wise proficiency-based recommendations
- Weak area detection
- Adaptive learning path generation
- Resource recommendations per topic
"""

LEARNING_RESOURCES = {
    "Mathematics": {
        "Algebra": {
            "beginner": ["Khan Academy: Algebra Basics", "3Blue1Brown: Essence of Linear Algebra"],
            "intermediate": ["MIT OCW: Linear Algebra", "Paul's Online Math Notes"],
            "advanced": ["Abstract Algebra - Dummit & Foote", "Artin's Algebra"]
        },
        "Calculus": {
            "beginner": ["Khan Academy: Calculus", "PatrickJMT YouTube Series"],
            "intermediate": ["MIT OCW 18.01: Single Variable Calculus", "Stewart Calculus"],
            "advanced": ["Spivak's Calculus", "Apostol's Mathematical Analysis"]
        },
        "Statistics": {
            "beginner": ["Khan Academy: Statistics", "StatQuest with Josh Starmer"],
            "intermediate": ["Introduction to Statistical Learning (ISLR)", "Think Stats"],
            "advanced": ["Elements of Statistical Learning (ESL)", "Bayesian Data Analysis"]
        }
    },
    "Physics": {
        "Mechanics": {
            "beginner": ["Khan Academy: Physics", "Walter Lewin Lectures (MIT)"],
            "intermediate": ["Halliday, Resnick & Krane", "Irodov Problems"],
            "advanced": ["Goldstein: Classical Mechanics", "Landau & Lifshitz Vol.1"]
        },
        "Quantum": {
            "beginner": ["Quantum Country (Matuschak & Nielsen)", "pHET Simulations"],
            "intermediate": ["Griffiths: QM", "Feynman Lectures Vol.3"],
            "advanced": ["Sakurai: Modern QM", "Weinberg: Lectures on QM"]
        }
    },
    "Computer Science": {
        "Algorithms": {
            "beginner": ["CS50 Harvard", "VisuAlgo.net"],
            "intermediate": ["CLRS: Introduction to Algorithms", "Sedgewick Algorithms"],
            "advanced": ["Knuth: TAOCP", "Competitive Programming 3"]
        },
        "Machine Learning": {
            "beginner": ["Andrew Ng ML Course (Coursera)", "fast.ai"],
            "intermediate": ["ESL / ISLR", "Hands-On ML with Scikit-Learn"],
            "advanced": ["Deep Learning - Goodfellow", "Pattern Recognition - Bishop"]
        },
        "Data Structures": {
            "beginner": ["CS50x", "Data Structures - mycodeschool YouTube"],
            "intermediate": ["Competitive Programming", "LeetCode patterns"],
            "advanced": ["Advanced Data Structures - MIT 6.851", "Research Papers"]
        }
    },
    "Chemistry": {
        "Organic": {
            "beginner": ["Khan Academy: Organic Chemistry", "Crash Course Chemistry"],
            "intermediate": ["Clayden: Organic Chemistry", "March's Advanced OC"],
            "advanced": ["Clayden Advanced Problems", "Carey & Sundberg"]
        },
        "Physical": {
            "beginner": ["Khan Academy: Chemistry", "Tyler DeWitt YouTube"],
            "intermediate": ["Atkins' Physical Chemistry", "Chang: Chemistry"],
            "advanced": ["McQuarrie: Statistical Mechanics", "Levine: Physical Chemistry"]
        }
    },
    "Biology": {
        "Cell Biology": {
            "beginner": ["Khan Academy: Biology", "Crash Course Biology"],
            "intermediate": ["Alberts: Molecular Biology of the Cell", "Lehninger Biochemistry"],
            "advanced": ["The Cell - Cooper", "Research Journals (Cell, Nature)"]
        },
        "Genetics": {
            "beginner": ["23andMe Education", "Kurzgesagt YouTube"],
            "intermediate": ["Strickberger's Genetics", "Lewin's Genes"],
            "advanced": ["Watson's Molecular Biology of the Gene", "Strachan & Read"]
        }
    }
}

MOTIVATIONAL_TIPS = {
    "struggling": [
        "🔥 Every expert was once a beginner. Break the topic into smaller chunks!",
        "💡 Try the Feynman Technique: explain the concept in simple words.",
        "⏰ Use the Pomodoro technique: 25 min focused study, 5 min break.",
        "🤝 Study groups help! Explain concepts to peers to reinforce learning.",
    ],
    "progressing": [
        "📈 Great progress! Challenge yourself with harder problems.",
        "🎯 You're getting it! Try applying concepts to real-world scenarios.",
        "⚡ Momentum is building — keep the streak going!",
    ],
    "mastered": [
        "🏆 Excellent mastery! Now help others — teaching reinforces learning.",
        "🚀 Ready for advanced topics! Push your boundaries.",
        "🌟 You're in the top 20% — explore research papers in this area.",
    ]
}


def get_proficiency_level(score: float) -> str:
    """Classify proficiency from score (0-100)."""
    if score < 35:
        return "beginner"
    elif score < 70:
        return "intermediate"
    else:
        return "advanced"


def get_proficiency_label(score: float) -> tuple:
    """Return (label, color, emoji) for UI display."""
    level = get_proficiency_level(score)
    mapping = {
        "beginner": ("Beginner", "#FF6B6B", "🌱"),
        "intermediate": ("Intermediate", "#FFD93D", "📚"),
        "advanced": ("Advanced", "#6BCB77", "🏆"),
    }
    return mapping[level]


def generate_recommendations(performance_data: list) -> dict:
    """
    Generate personalized topic recommendations.
    performance_data: list of {topic, proficiency_score, attempts}
    """
    if not performance_data:
        # New student — recommend all topics
        from modules.quiz_engine import get_all_topics
        topics = get_all_topics()
        return {
            "priority_topics": topics[:3],
            "suggested_content": {},
            "weak_areas": [],
            "strong_areas": [],
            "next_steps": ["Start with any topic that interests you!"],
            "study_tip": MOTIVATIONAL_TIPS["struggling"][0],
            "overall_level": "beginner"
        }
    
    # Classify each topic
    weak_areas = [p for p in performance_data if (p.get("proficiency_score") or 0) < 40]
    moderate_areas = [p for p in performance_data if 40 <= (p.get("proficiency_score") or 0) < 70]
    strong_areas = [p for p in performance_data if (p.get("proficiency_score") or 0) >= 70]
    
    # Sort by score ascending — recommend weakest first
    weak_areas_sorted = sorted(weak_areas, key=lambda x: (x.get("proficiency_score") or 0))
    
    # Priority: weak topics → moderate topics → new topics
    priority_topics = [p["topic"] for p in weak_areas_sorted[:3]]
    
    # Generate resources for each topic
    suggested_content = {}
    for perf in performance_data:
        topic = perf["topic"]
        score = perf.get("proficiency_score") or 0
        level = get_proficiency_level(score)
        resources = LEARNING_RESOURCES.get(topic, {})
        # Get first subtopic resources
        all_resources = []
        for subtopic_resources in resources.values():
            all_resources.extend(subtopic_resources.get(level, []))
        suggested_content[topic] = {
            "level": level,
            "score": score,
            "resources": all_resources[:3]
        }
    
    # Overall level based on average score
    avg_score = sum((p.get("proficiency_score") or 0) for p in performance_data) / len(performance_data)
    overall_level = get_proficiency_level(avg_score)
    
    # Next steps
    next_steps = []
    if weak_areas:
        next_steps.append(f"Focus on: {', '.join([p['topic'] for p in weak_areas[:2]])}")
    if moderate_areas:
        next_steps.append(f"Improve: {', '.join([p['topic'] for p in moderate_areas[:2]])}")
    if strong_areas:
        next_steps.append(f"Advance: {', '.join([p['topic'] for p in strong_areas[:2]])}")
    
    # Study tip
    if avg_score < 40:
        tip = MOTIVATIONAL_TIPS["struggling"][len(weak_areas) % len(MOTIVATIONAL_TIPS["struggling"])]
    elif avg_score < 70:
        tip = MOTIVATIONAL_TIPS["progressing"][0]
    else:
        tip = MOTIVATIONAL_TIPS["mastered"][0]
    
    return {
        "priority_topics": priority_topics or [p["topic"] for p in performance_data[:3]],
        "suggested_content": suggested_content,
        "weak_areas": [p["topic"] for p in weak_areas],
        "moderate_areas": [p["topic"] for p in moderate_areas],
        "strong_areas": [p["topic"] for p in strong_areas],
        "next_steps": next_steps,
        "study_tip": tip,
        "overall_level": overall_level,
        "avg_score": round(avg_score, 1)
    }


def get_adaptive_difficulty(topic: str, performance_data: list) -> int:
    """Return recommended difficulty (1-5) for next quiz based on performance."""
    topic_perf = next((p for p in performance_data if p["topic"] == topic), None)
    if not topic_perf:
        return 2  # Default to easy-medium
    score = topic_perf["proficiency_score"]
    if score < 30:
        return 1
    elif score < 50:
        return 2
    elif score < 70:
        return 3
    elif score < 85:
        return 4
    else:
        return 5


def get_learning_path(performance_data: list) -> list:
    """Generate a structured learning path."""
    from modules.quiz_engine import get_all_topics
    all_topics = get_all_topics()
    
    attempted = {p["topic"]: p["proficiency_score"] for p in performance_data}
    
    path = []
    for topic in all_topics:
        score = attempted.get(topic, 0)
        level = get_proficiency_level(score)
        status = "completed" if score >= 70 else "in_progress" if score > 0 else "not_started"
        path.append({
            "topic": topic,
            "score": score,
            "level": level,
            "status": status,
            "recommended_difficulty": get_adaptive_difficulty(topic, performance_data)
        })
    
    # Sort: in_progress first, then not_started, then completed
    order = {"in_progress": 0, "not_started": 1, "completed": 2}
    path.sort(key=lambda x: (order[x["status"]], -x["score"]))
    return path
