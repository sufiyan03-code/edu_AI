"""
AI Chatbot Tutor Module
Rule-based + pattern matching intelligent tutor.
"""
import random
import re
from datetime import datetime

# Subject knowledge base
KNOWLEDGE_BASE = {
    "newton": "Newton's Laws of Motion:\n1️⃣ **Inertia**: An object stays at rest or uniform motion unless acted on by a force.\n2️⃣ **F = ma**: Force equals mass times acceleration.\n3️⃣ **Action-Reaction**: For every action, there is an equal and opposite reaction.",
    "newton's law": "Newton's Laws of Motion:\n1️⃣ **Inertia**: An object stays at rest or uniform motion unless acted on by a force.\n2️⃣ **F = ma**: Force equals mass times acceleration.\n3️⃣ **Action-Reaction**: For every action, there is an equal and opposite reaction.",
    "derivative": "A **derivative** measures the rate of change of a function.\n- **Power Rule**: d/dx(xⁿ) = nxⁿ⁻¹\n- **Chain Rule**: d/dx[f(g(x))] = f'(g(x))·g'(x)\n- **Product Rule**: (uv)' = u'v + uv'\n\nExample: d/dx(x³) = 3x²",
    "integral": "An **integral** is the reverse of differentiation and measures area under a curve.\n- **Power Rule**: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C\n- **Definite integral**: gives a specific number (area between bounds)\n\nExample: ∫2x dx = x² + C",
    "oop": "**Object-Oriented Programming** key concepts:\n- **Encapsulation**: Bundling data + methods in a class\n- **Inheritance**: Child class inherits parent class features\n- **Polymorphism**: Same interface, different implementations\n- **Abstraction**: Hiding complex implementation details",
    "recursion": "**Recursion** is when a function calls itself.\n```python\ndef factorial(n):\n    if n == 0:  # base case\n        return 1\n    return n * factorial(n-1)  # recursive case\n```\nKey parts: **Base case** (stops recursion) + **Recursive case**",
    "dna": "**DNA (Deoxyribonucleic Acid)**:\n- Double helix structure discovered by Watson & Crick (1953)\n- Made of **nucleotides**: A, T, G, C\n- Base pairs: A-T and G-C\n- Carries genetic information for all living organisms",
    "photosynthesis": "**Photosynthesis**: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂\n- Occurs in **chloroplasts** using **chlorophyll**\n- **Light reactions**: occur in thylakoids, produce ATP\n- **Calvin cycle**: occurs in stroma, produces glucose",
    "machine learning": "**Machine Learning** types:\n- **Supervised**: Learn from labeled data (classification, regression)\n- **Unsupervised**: Find patterns in unlabeled data (clustering)\n- **Reinforcement**: Learn by reward/punishment interactions\n\nKey algorithms: Linear Regression, Decision Trees, Neural Networks, SVM",
    "big o": "**Big-O Notation** measures algorithm efficiency:\n- O(1) — Constant (best)\n- O(log n) — Logarithmic (Binary Search)\n- O(n) — Linear (Linear Search)\n- O(n log n) — Linearithmic (MergeSort)\n- O(n²) — Quadratic (Bubble Sort)\n- O(2ⁿ) — Exponential (worst)",
    "sorting": "**Sorting Algorithms**:\n| Algorithm | Best | Avg | Worst |\n|-----------|------|-----|-------|\n| Bubble Sort | O(n) | O(n²) | O(n²) |\n| Merge Sort | O(n log n) | O(n log n) | O(n log n) |\n| Quick Sort | O(n log n) | O(n log n) | O(n²) |\n| Insertion Sort | O(n) | O(n²) | O(n²) |",
    "acid": "**Acids and Bases**:\n- **Acid**: proton donor, pH < 7 (e.g., HCl, H₂SO₄)\n- **Base**: proton acceptor, pH > 7 (e.g., NaOH, NH₃)\n- **Neutralization**: Acid + Base → Salt + Water\n- **pH formula**: pH = -log[H⁺]",
    "osmosis": "**Osmosis**: Movement of water through a selectively permeable membrane from lower to higher solute concentration.\n- **Hypertonic**: More solute outside → cell shrinks\n- **Hypotonic**: More solute inside → cell swells\n- **Isotonic**: Equal solute → no net movement",
    "entropy": "**Entropy** (S): Measure of disorder/randomness in a system.\n- 2nd Law of Thermodynamics: total entropy of a system always increases.\n- ΔS > 0: spontaneous\n- Gibbs Free Energy: ΔG = ΔH - TΔS\n- At equilibrium: ΔG = 0",
    "matrix": "**Matrices** — rectangular arrays of numbers:\n- **Addition**: element-wise (same dimensions)\n- **Multiplication**: A(m×n) × B(n×p) = C(m×p)\n- **Determinant**: |A| = ad - bc for 2×2\n- **Inverse**: A⁻¹ exists when det(A) ≠ 0\n- Used in: computer graphics, machine learning, physics simulations",
    "probability": "**Probability**:\n- P(A) = favorable outcomes / total outcomes\n- 0 ≤ P(A) ≤ 1\n- **Addition rule**: P(A∪B) = P(A) + P(B) - P(A∩B)\n- **Multiplication rule**: P(A∩B) = P(A)·P(B|A)\n- **Bayes' theorem**: P(A|B) = P(B|A)·P(A)/P(B)",
    "cell": "**Cell Types**:\n- **Prokaryotic**: No nucleus, no membrane-bound organelles (bacteria)\n- **Eukaryotic**: Has nucleus and organelles (animals, plants, fungi)\n\n**Key organelles**:\n- Nucleus: control center\n- Mitochondria: energy production\n- Ribosome: protein synthesis\n- Endoplasmic Reticulum: transport",
}

GREETINGS = [
    "Hello! I'm your AI Tutor 🤖 I can help with Mathematics, Physics, Chemistry, Biology, and Computer Science. What would you like to learn today?",
    "Hi there! Ready to learn? I cover Mathematics, Physics, Chemistry, Biology, and Computer Science. Ask me anything! 🎓",
    "Welcome! I'm here to help you understand complex topics. What subject are you studying? 📚"
]

CONFUSED_RESPONSES = [
    "I'm not sure I understand that question. Could you rephrase it? I can help with topics like Newton's Laws, derivatives, integrals, DNA, photosynthesis, Big-O notation, and more!",
    "That's a bit unclear to me. Try asking about specific topics like 'explain recursion', 'what is DNA', or 'how does photosynthesis work'?",
    "I didn't quite catch that. Ask me something like: 'explain machine learning', 'what is entropy', or 'help with derivatives'!"
]

ENCOURAGEMENT = [
    "Great question! 🌟", "Excellent curiosity! 💡", "That's a fundamental concept! 🎯",
    "Good thinking! 🧠", "Let me explain! 📖"
]


def find_best_answer(user_message: str) -> str:
    """Find the best answer from knowledge base."""
    msg_lower = user_message.lower().strip()
    
    # Direct keyword matching with word boundaries
    for key, answer in KNOWLEDGE_BASE.items():
        pattern = r'\b' + re.escape(key) + r'\b'
        if re.search(pattern, msg_lower):
            intro = random.choice(ENCOURAGEMENT)
            return f"{intro}\n\n{answer}"
    
    # Partial matches with whole-word token matching
    words = set(re.findall(r'\b\w+\b', msg_lower))
    best_key = None
    best_score = 0
    for key in KNOWLEDGE_BASE:
        key_words = set(key.split())
        # Count matching full words
        score = len(key_words & words)
        if score > best_score:
            best_score = score
            best_key = key
    
    if best_score > 0 and best_key:
        intro = random.choice(ENCOURAGEMENT)
        return f"{intro}\n\n{KNOWLEDGE_BASE[best_key]}"
    
    return None


def get_subject_help(subject: str) -> str:
    """Return overview of what help is available for a subject."""
    subject_topics = {
        "mathematics": "📐 **Mathematics topics I can explain**:\n- Derivatives & Integrals (Calculus)\n- Matrices & Linear Algebra\n- Probability & Statistics\n- Sequences & Series\n\nAsk: 'explain derivative' or 'what is probability'",
        "physics": "⚛️ **Physics topics I can explain**:\n- Newton's Laws of Motion\n- Thermodynamics & Entropy\n- Waves & Optics\n- Quantum Mechanics basics\n\nAsk: 'explain newton's law' or 'what is entropy'",
        "chemistry": "🧪 **Chemistry topics I can explain**:\n- Acids and Bases\n- Chemical Bonding\n- Thermodynamics\n- Organic Chemistry\n\nAsk: 'explain acid base' or 'what is entropy'",
        "biology": "🧬 **Biology topics I can explain**:\n- Cell Structure & Function\n- DNA & Genetics\n- Photosynthesis\n- Osmosis & Diffusion\n\nAsk: 'explain dna' or 'what is photosynthesis'",
        "computer science": "💻 **CS topics I can explain**:\n- Big-O Notation & Complexity\n- Sorting Algorithms\n- OOP Concepts\n- Recursion\n- Machine Learning\n\nAsk: 'explain recursion' or 'what is Big O'"
    }
    return subject_topics.get(subject, None)


def process_special_commands(msg: str) -> str:
    """Handle special chatbot commands."""
    msg_lower = msg.lower().strip()
    
    # Greetings
    if any(word in msg_lower for word in ["hi", "hello", "hey", "howdy", "greetings"]):
        return random.choice(GREETINGS)
    
    # How are you
    if any(p in msg_lower for p in ["how are you", "how r u", "how do you do"]):
        return "I'm doing great and ready to help you learn! 🚀 What topic would you like to explore today?"
    
    # Thanks
    if any(word in msg_lower for word in ["thank", "thanks", "thx", "ty"]):
        return "You're welcome! 🎉 Keep learning — you're doing amazing! Is there anything else you'd like to know?"
    
    # Help
    if msg_lower in ["help", "help me", "what can you do", "assist"]:
        return ("I'm your AI Tutor! Here's what I can do:\n\n"
                "📚 **Explain concepts** in: Mathematics, Physics, Chemistry, Biology, CS\n"
                "🧮 **Help with formulas** and step-by-step explanations\n"
                "💡 **Answer questions** about almost any STEM topic\n\n"
                "Try asking:\n- 'Explain Newton's laws'\n- 'What is recursion?'\n- 'How does photosynthesis work?'\n- 'What is machine learning?'")
    
    # Subject overviews
    for subj in ["mathematics", "physics", "chemistry", "biology", "computer science"]:
        if subj in msg_lower and any(w in msg_lower for w in ["help", "topics", "what", "teach", "learn"]):
            result = get_subject_help(subj)
            if result:
                return result
    
    return None


def generate_quiz_hint(topic: str, score: float) -> str:
    """Generate a hint based on topic and performance."""
    hints = {
        "Mathematics": [
            "💡 Remember to check your work by substituting back into the original equation!",
            "📐 Draw a diagram when dealing with geometry problems — it often reveals the solution.",
            "🔢 For calculus, practice the basic rules daily: power rule, chain rule, product rule."
        ],
        "Physics": [
            "⚛️ Always identify what's given and what you're looking for before solving.",
            "📊 Free body diagrams help visualize forces in mechanics problems.",
            "🌊 Remember: waves transfer energy, not matter."
        ],
        "Computer Science": [
            "💻 Trace through your algorithm manually with a small example first.",
            "🔄 For recursion, define the base case before the recursive case.",
            "📊 Practice drawing data structures on paper to understand them deeply."
        ],
        "Chemistry": [
            "⚗️ Balance chemical equations by checking atoms on both sides.",
            "🧪 Remember: acids donate protons, bases accept protons (Brønsted-Lowry).",
            "📈 Use Le Chatelier's principle: equilibrium shifts to counteract changes."
        ],
        "Biology": [
            "🧬 Create mnemonics for complex processes like the Krebs cycle.",
            "🔬 Connect cellular processes to everyday phenomena — it helps you remember!",
            "🌱 Understanding evolution helps make sense of all of biology."
        ]
    }
    
    topic_hints = hints.get(topic, ["Keep practicing! Consistent effort leads to mastery. 🌟"])
    hint = random.choice(topic_hints)
    
    if score < 40:
        return f"📌 **Study Tip**: {hint}\n\n🎯 Your score is below 40% — focus on fundamentals first!"
    elif score < 70:
        return f"📌 **Study Tip**: {hint}\n\n📈 Good progress! You're in the intermediate zone."
    else:
        return f"📌 **Study Tip**: {hint}\n\n🏆 Excellent score! Challenge yourself with harder problems!"


def get_bot_response(user_message: str, topic_context: str = "", performance_score: float = 50.0) -> str:
    """
    Main chatbot response function.
    """
    if not user_message or not user_message.strip():
        return "Please ask me a question! I'm here to help. 😊"
    
    # Special commands
    special_response = process_special_commands(user_message)
    if special_response:
        return special_response
    
    # Check for hint/tip requests
    msg_lower = user_message.lower()
    if any(word in msg_lower for word in ["hint", "tip", "advice", "help me study"]):
        if topic_context:
            return generate_quiz_hint(topic_context, performance_score)
    
    # Check for "what is", "explain", "tell me about", "how does" patterns
    is_question = any(msg_lower.startswith(p) for p in [
        "what", "how", "why", "explain", "tell me", "describe", "define",
        "can you", "could you", "please"
    ])
    
    # Knowledge base lookup
    answer = find_best_answer(user_message)
    if answer:
        return answer
    
    # Topic-specific fallback
    if topic_context and is_question:
        return (f"That's a great question about {topic_context}! 🤔\n\n"
                f"I don't have a specific answer for that exact query, but here's what I suggest:\n"
                f"1. Review your textbook chapter on {topic_context}\n"
                f"2. Search Khan Academy for step-by-step explanations\n"
                f"3. Try solving similar practice problems\n\n"
                f"Would you like me to explain any specific concept within {topic_context}?")
    
    # General fallback
    return random.choice(CONFUSED_RESPONSES)
