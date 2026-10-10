"""
NLP Analyzer Module
- Sentiment analysis on student responses
- TF-IDF keyword extraction
- Answer similarity scoring
- Confusion/confidence detection
"""
import re
import math
from collections import Counter

# Simple but effective NLP without heavyweight dependencies at import time
POSITIVE_WORDS = {
    'understand', 'understood', 'clear', 'easy', 'got', 'know', 'confident',
    'sure', 'correct', 'right', 'great', 'good', 'excellent', 'perfect',
    'simple', 'obvious', 'makes sense', 'learned', 'mastered'
}

NEGATIVE_WORDS = {
    'confused', 'confusing', 'difficult', 'hard', 'don\'t know', 'dont know',
    'unsure', 'uncertain', 'lost', 'struggling', 'stuck', 'help', 'wrong',
    'mistake', 'error', 'problem', 'trouble', 'unclear', 'don\'t understand',
    'complicated', 'complex', 'haven\'t', 'forgot', 'forget', 'not sure'
}


SUBJECT_KEYWORDS = {
    "Mathematics": ["equation", "formula", "algebra", "calculus", "derivative", "integral",
                    "matrix", "vector", "theorem", "proof", "function", "limit", "series",
                    "probability", "statistics", "geometry", "trigonometry"],
    "Physics": ["force", "energy", "momentum", "velocity", "acceleration", "mass",
                "charge", "field", "wave", "quantum", "relativity", "thermodynamics",
                "entropy", "photon", "electron", "gravitational"],
    "Chemistry": ["element", "compound", "reaction", "bond", "molecule", "atom",
                  "periodic", "oxidation", "reduction", "acid", "base", "entropy",
                  "enthalpy", "polymer", "organic", "inorganic"],
    "Computer Science": ["algorithm", "data structure", "recursion", "loop", "function",
                         "class", "object", "pointer", "memory", "complexity", "sorting",
                         "graph", "tree", "hash", "binary", "hexadecimal", "network"],
    "Biology": ["cell", "dna", "rna", "protein", "evolution", "gene", "chromosome",
                "mitosis", "meiosis", "photosynthesis", "respiration", "enzyme",
                "membrane", "organism", "ecosystem", "species"]
}


def preprocess_text(text: str) -> list:
    """Clean and tokenize text."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = text.split()
    # Remove very short tokens
    tokens = [t for t in tokens if len(t) > 2]
    return tokens


def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment of student response text.
    Returns score from -1 (very negative) to +1 (very positive).
    """
    if not text or not text.strip():
        return {"score": 0.0, "label": "Neutral", "confidence": 0.5}
    
    tokens = preprocess_text(text)
    text_lower = text.lower()
    
    pos_count = sum(1 for w in POSITIVE_WORDS if w in text_lower)
    neg_count = sum(1 for w in NEGATIVE_WORDS if w in text_lower)
    
    total = pos_count + neg_count
    if total == 0:
        score = 0.0
        label = "Neutral"
        confidence = 0.5
    else:
        score = (pos_count - neg_count) / total
        if score > 0.3:
            label = "Confident"
        elif score < -0.3:
            label = "Confused"
        else:
            label = "Neutral"
        confidence = abs(score) * 0.5 + 0.5
    
    return {
        "score": round(score, 3),
        "label": label,
        "confidence": round(confidence, 3),
        "positive_signals": pos_count,
        "negative_signals": neg_count
    }


def extract_keywords(text: str, top_n: int = 10) -> list:
    """Extract important keywords using TF-IDF-like scoring."""
    if not text or not text.strip():
        return []
    
    tokens = preprocess_text(text)
    if not tokens:
        return []
    
    # Count term frequency
    tf = Counter(tokens)
    total_terms = len(tokens)
    
    # Simple IDF weights (common stop words get lower weight)
    stop_words = {'the','and','for','are','but','not','you','all','can','had',
                  'her','was','one','our','out','day','get','has','him','his',
                  'how','its','may','new','now','old','see','two','way','who',
                  'did','with','this','that','have','from','they','will','been',
                  'were','said','each','she','which','when','their'}
    
    scored = {}
    for term, freq in tf.items():
        if term in stop_words:
            continue
        tf_score = freq / total_terms
        # Boost longer, more specific terms
        length_bonus = min(len(term) / 10, 0.5)
        scored[term] = tf_score + length_bonus
    
    sorted_terms = sorted(scored.items(), key=lambda x: x[1], reverse=True)
    return [{"word": w, "score": round(s, 4)} for w, s in sorted_terms[:top_n]]


def compute_text_similarity(text1: str, text2: str) -> float:
    """Compute cosine similarity between two texts using TF vectors."""
    if not text1 or not text2:
        return 0.0
    
    tokens1 = set(preprocess_text(text1))
    tokens2 = set(preprocess_text(text2))
    
    if not tokens1 or not tokens2:
        return 0.0
    
    intersection = tokens1 & tokens2
    similarity = len(intersection) / math.sqrt(len(tokens1) * len(tokens2))
    return round(similarity, 4)


def detect_topic_from_text(text: str) -> str:
    """Detect which subject a text is about."""
    if not text:
        return "General"
    
    text_lower = text.lower()
    scores = {}
    for subject, keywords in SUBJECT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[subject] = score
    
    if not scores:
        return "General"
    return max(scores, key=scores.get)


def analyze_answer_quality(user_answer: str, correct_answer: str, topic: str = "") -> dict:
    """
    Comprehensive analysis of a student's answer vs correct answer.
    """
    sentiment = analyze_sentiment(user_answer)
    keywords = extract_keywords(user_answer, top_n=5)
    similarity = compute_text_similarity(user_answer, correct_answer)
    detected_topic = detect_topic_from_text(user_answer) if user_answer else topic
    
    # Quality score (0-100)
    quality = min(100, int(similarity * 100 + sentiment["confidence"] * 20))
    
    # Feedback generation
    if similarity > 0.7:
        feedback = "Excellent! Your answer closely matches the expected response."
    elif similarity > 0.4:
        feedback = "Good attempt! You captured some key concepts."
    elif similarity > 0.2:
        feedback = "Partial understanding shown. Review the topic further."
    else:
        feedback = "Your answer needs improvement. Study the core concepts."
    
    if sentiment["label"] == "Confused":
        feedback += " You seem uncertain — consider revisiting the fundamentals."
    elif sentiment["label"] == "Confident":
        feedback += " Great confidence shown in your response!"
    
    return {
        "sentiment": sentiment,
        "keywords": keywords,
        "similarity_score": similarity,
        "quality_score": quality,
        "feedback": feedback,
        "detected_topic": detected_topic
    }


def generate_nlp_insights(answers: list) -> dict:
    """
    Generate aggregate NLP insights from a list of answer dictionaries.
    Each dict should have 'response_text', 'sentiment_score', 'is_correct'.
    """
    if not answers:
        return {}
    
    all_text = " ".join([(a.get("response_text") or "") for a in answers if a.get("response_text")])
    
    avg_sentiment = (
        sum((a.get("sentiment_score") or 0) for a in answers) / len(answers)
        if answers else 0
    )
    
    correct_answers = [a for a in answers if a.get("is_correct")]
    wrong_answers = [a for a in answers if not a.get("is_correct")]
    
    correct_text = " ".join([(a.get("response_text") or "") for a in correct_answers if a.get("response_text")])
    wrong_text = " ".join([(a.get("response_text") or "") for a in wrong_answers if a.get("response_text")])
    
    top_keywords = extract_keywords(all_text, top_n=15)
    confused_keywords = extract_keywords(wrong_text, top_n=8)
    strong_keywords = extract_keywords(correct_text, top_n=8)
    
    # Confusion patterns
    confusion_signals = []
    for a in answers:
        rt = (a.get("response_text") or "").lower()
        for neg in NEGATIVE_WORDS:
            if neg in rt:
                confusion_signals.append(neg)
    
    confusion_freq = Counter(confusion_signals).most_common(5)
    
    overall_mood = "Confident" if avg_sentiment > 0.2 else "Struggling" if avg_sentiment < -0.2 else "Neutral"
    
    return {
        "overall_sentiment": round(avg_sentiment, 3),
        "overall_mood": overall_mood,
        "top_keywords": top_keywords,
        "confused_keywords": confused_keywords,
        "strong_keywords": strong_keywords,
        "confusion_patterns": confusion_freq,
        "total_responses": len([a for a in answers if a.get("response_text")]),
    }
