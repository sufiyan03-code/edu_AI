"""
Question Bank — comprehensive adaptive quiz content across 5 subjects.
Each question has: id, topic, subtopic, question, options, correct, explanation, difficulty (1-5)
"""
import json

QUESTION_BANK = {
    "Mathematics": [
        {
            "id": "math_001", "topic": "Mathematics", "subtopic": "Algebra",
            "question": "What is the solution to the equation 2x + 6 = 14?",
            "options": ["x = 3", "x = 4", "x = 5", "x = 6"],
            "correct": "x = 4",
            "explanation": "Subtract 6 from both sides: 2x = 8, then divide by 2: x = 4.",
            "difficulty": 1
        },
        {
            "id": "math_002", "topic": "Mathematics", "subtopic": "Quadratics",
            "question": "What are the roots of x² - 5x + 6 = 0?",
            "options": ["x = 2, 3", "x = -2, -3", "x = 1, 6", "x = -1, -6"],
            "correct": "x = 2, 3",
            "explanation": "Factor as (x-2)(x-3) = 0, so x = 2 or x = 3.",
            "difficulty": 2
        },
        {
            "id": "math_003", "topic": "Mathematics", "subtopic": "Calculus",
            "question": "What is the derivative of f(x) = x³ + 2x²?",
            "options": ["3x² + 4x", "3x + 4", "x² + 4x", "3x² + 2x"],
            "correct": "3x² + 4x",
            "explanation": "Applying power rule: d/dx(x³)=3x², d/dx(2x²)=4x.",
            "difficulty": 3
        },
        {
            "id": "math_004", "topic": "Mathematics", "subtopic": "Linear Algebra",
            "question": "What is the determinant of [[2, 3], [1, 4]]?",
            "options": ["5", "8", "11", "2"],
            "correct": "5",
            "explanation": "det = (2×4) - (3×1) = 8 - 3 = 5.",
            "difficulty": 3
        },
        {
            "id": "math_005", "topic": "Mathematics", "subtopic": "Probability",
            "question": "Two dice are rolled. What is P(sum = 7)?",
            "options": ["1/6", "5/36", "7/36", "1/12"],
            "correct": "1/6",
            "explanation": "There are 6 ways to get sum 7 out of 36 total outcomes: 6/36 = 1/6.",
            "difficulty": 2
        },
        {
            "id": "math_006", "topic": "Mathematics", "subtopic": "Calculus",
            "question": "What is ∫(2x + 3)dx?",
            "options": ["x² + 3x + C", "2x² + 3x + C", "x² + C", "2 + C"],
            "correct": "x² + 3x + C",
            "explanation": "Integrate term by term: ∫2x dx = x², ∫3 dx = 3x, plus constant C.",
            "difficulty": 3
        },
        {
            "id": "math_007", "topic": "Mathematics", "subtopic": "Statistics",
            "question": "The mean of 5 numbers is 10. If 4 numbers are 8,12,9,11, what is the 5th?",
            "options": ["10", "9", "11", "12"],
            "correct": "10",
            "explanation": "Sum = 5×10 = 50. Known sum = 8+12+9+11 = 40. 5th = 50-40 = 10.",
            "difficulty": 2
        },
        {
            "id": "math_008", "topic": "Mathematics", "subtopic": "Geometry",
            "question": "What is the area of a circle with radius 7 (use π ≈ 3.14)?",
            "options": ["153.86", "43.96", "49", "21.98"],
            "correct": "153.86",
            "explanation": "Area = πr² = 3.14 × 49 = 153.86.",
            "difficulty": 1
        },
        {
            "id": "math_009", "topic": "Mathematics", "subtopic": "Numbers",
            "question": "What is the value of 2¹⁰?",
            "options": ["1024", "512", "2048", "256"],
            "correct": "1024",
            "explanation": "2¹⁰ = 1024 (often memorized in CS as 1K).",
            "difficulty": 1
        },
        {
            "id": "math_010", "topic": "Mathematics", "subtopic": "Sequences",
            "question": "What is the 10th term of the arithmetic sequence 3, 7, 11, 15, ...?",
            "options": ["39", "43", "35", "47"],
            "correct": "39",
            "explanation": "aₙ = a₁ + (n-1)d = 3 + 9×4 = 3 + 36 = 39.",
            "difficulty": 2
        },
        {
            "id": "math_011", "topic": "Mathematics", "subtopic": "Trigonometry",
            "question": "What is sin(30°)?",
            "options": ["0.5", "√3/2", "1/√2", "1"],
            "correct": "0.5",
            "explanation": "sin(30°) = 1/2 = 0.5 (standard value).",
            "difficulty": 1
        },
        {
            "id": "math_012", "topic": "Mathematics", "subtopic": "Complex Numbers",
            "question": "What is i² where i = √(-1)?",
            "options": ["-1", "1", "i", "-i"],
            "correct": "-1",
            "explanation": "By definition, i = √(-1), so i² = -1.",
            "difficulty": 2
        },
    ],
    "Physics": [
        {
            "id": "phy_001", "topic": "Physics", "subtopic": "Mechanics",
            "question": "What is Newton's Second Law of Motion?",
            "options": ["F = ma", "F = mv", "F = m/a", "F = ma²"],
            "correct": "F = ma",
            "explanation": "Force equals mass times acceleration: F = ma.",
            "difficulty": 1
        },
        {
            "id": "phy_002", "topic": "Physics", "subtopic": "Energy",
            "question": "What is the kinetic energy of a 2kg object moving at 3 m/s?",
            "options": ["9 J", "6 J", "18 J", "3 J"],
            "correct": "9 J",
            "explanation": "KE = ½mv² = ½ × 2 × 3² = 9 J.",
            "difficulty": 2
        },
        {
            "id": "phy_003", "topic": "Physics", "subtopic": "Waves",
            "question": "The speed of light in vacuum is approximately:",
            "options": ["3×10⁸ m/s", "3×10⁶ m/s", "3×10¹⁰ m/s", "3×10⁴ m/s"],
            "correct": "3×10⁸ m/s",
            "explanation": "c ≈ 2.998 × 10⁸ m/s, commonly approximated as 3×10⁸ m/s.",
            "difficulty": 1
        },
        {
            "id": "phy_004", "topic": "Physics", "subtopic": "Thermodynamics",
            "question": "Which law states that energy cannot be created or destroyed?",
            "options": ["1st Law of Thermodynamics", "2nd Law of Thermodynamics", "Newton's 3rd Law", "Ohm's Law"],
            "correct": "1st Law of Thermodynamics",
            "explanation": "The First Law of Thermodynamics is the law of conservation of energy.",
            "difficulty": 1
        },
        {
            "id": "phy_005", "topic": "Physics", "subtopic": "Electricity",
            "question": "Ohm's Law states V = IR. If R = 5Ω and I = 2A, what is V?",
            "options": ["10 V", "2.5 V", "7 V", "0.4 V"],
            "correct": "10 V",
            "explanation": "V = IR = 2 × 5 = 10 Volts.",
            "difficulty": 1
        },
        {
            "id": "phy_006", "topic": "Physics", "subtopic": "Quantum",
            "question": "What does the Heisenberg Uncertainty Principle state?",
            "options": [
                "We cannot know both position and momentum precisely simultaneously",
                "Energy is quantized",
                "Light behaves as both wave and particle",
                "Mass and energy are equivalent"
            ],
            "correct": "We cannot know both position and momentum precisely simultaneously",
            "explanation": "ΔxΔp ≥ ℏ/2 — the more precisely position is known, the less precisely momentum can be known.",
            "difficulty": 3
        },
        {
            "id": "phy_007", "topic": "Physics", "subtopic": "Mechanics",
            "question": "What is the acceleration due to gravity on Earth's surface?",
            "options": ["9.8 m/s²", "9.8 m/s", "10 m/s²", "9.8 km/s²"],
            "correct": "9.8 m/s²",
            "explanation": "g ≈ 9.8 m/s² (often approximated as 10 m/s²).",
            "difficulty": 1
        },
        {
            "id": "phy_008", "topic": "Physics", "subtopic": "Optics",
            "question": "Which phenomenon explains why a pencil appears bent in water?",
            "options": ["Refraction", "Reflection", "Diffraction", "Dispersion"],
            "correct": "Refraction",
            "explanation": "Light bends when passing between media of different densities (Snell's Law).",
            "difficulty": 2
        },
        {
            "id": "phy_009", "topic": "Physics", "subtopic": "Relativity",
            "question": "Einstein's mass-energy equivalence is expressed as:",
            "options": ["E = mc²", "E = mv²", "E = m/c²", "E = mc"],
            "correct": "E = mc²",
            "explanation": "E = mc², where c is the speed of light, is one of the most famous equations.",
            "difficulty": 2
        },
        {
            "id": "phy_010", "topic": "Physics", "subtopic": "Waves",
            "question": "What is the frequency of a wave that has a period of 0.02 seconds?",
            "options": ["50 Hz", "0.02 Hz", "20 Hz", "100 Hz"],
            "correct": "50 Hz",
            "explanation": "f = 1/T = 1/0.02 = 50 Hz.",
            "difficulty": 2
        },
        {
            "id": "phy_011", "topic": "Physics", "subtopic": "Magnetism",
            "question": "What is the SI unit of magnetic flux density?",
            "options": ["Tesla", "Weber", "Gauss", "Henry"],
            "correct": "Tesla",
            "explanation": "Magnetic flux density B is measured in Tesla (T). 1 T = 1 Wb/m².",
            "difficulty": 3
        },
        {
            "id": "phy_012", "topic": "Physics", "subtopic": "Mechanics",
            "question": "A car accelerates from 0 to 60 m/s in 10 seconds. What is the acceleration?",
            "options": ["6 m/s²", "60 m/s²", "600 m/s²", "0.6 m/s²"],
            "correct": "6 m/s²",
            "explanation": "a = (v-u)/t = (60-0)/10 = 6 m/s².",
            "difficulty": 1
        },
    ],
    "Computer Science": [
        {
            "id": "cs_001", "topic": "Computer Science", "subtopic": "Big-O",
            "question": "What is the time complexity of Binary Search?",
            "options": ["O(log n)", "O(n)", "O(n²)", "O(1)"],
            "correct": "O(log n)",
            "explanation": "Binary search halves the search space each step → O(log n).",
            "difficulty": 2
        },
        {
            "id": "cs_002", "topic": "Computer Science", "subtopic": "Data Structures",
            "question": "Which data structure uses LIFO (Last In, First Out)?",
            "options": ["Stack", "Queue", "Heap", "Graph"],
            "correct": "Stack",
            "explanation": "A stack follows LIFO — the last element pushed is the first popped.",
            "difficulty": 1
        },
        {
            "id": "cs_003", "topic": "Computer Science", "subtopic": "Machine Learning",
            "question": "Which algorithm is best for labeled classification data?",
            "options": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Semi-supervised"],
            "correct": "Supervised Learning",
            "explanation": "Supervised learning uses labeled examples to train a classifier.",
            "difficulty": 2
        },
        {
            "id": "cs_004", "topic": "Computer Science", "subtopic": "Networking",
            "question": "What does HTTP stand for?",
            "options": [
                "HyperText Transfer Protocol",
                "High Transfer Text Protocol",
                "HyperText Transmission Protocol",
                "Hosted Text Transfer Protocol"
            ],
            "correct": "HyperText Transfer Protocol",
            "explanation": "HTTP = HyperText Transfer Protocol, basis of web communication.",
            "difficulty": 1
        },
        {
            "id": "cs_005", "topic": "Computer Science", "subtopic": "OOP",
            "question": "What does 'polymorphism' mean in OOP?",
            "options": [
                "Objects of different types can be treated as objects of a common type",
                "A class can only have one method",
                "An object can only belong to one class",
                "Methods must always return values"
            ],
            "correct": "Objects of different types can be treated as objects of a common type",
            "explanation": "Polymorphism allows different object types to share an interface.",
            "difficulty": 2
        },
        {
            "id": "cs_006", "topic": "Computer Science", "subtopic": "Algorithms",
            "question": "What is the worst-case time complexity of QuickSort?",
            "options": ["O(n²)", "O(n log n)", "O(log n)", "O(n)"],
            "correct": "O(n²)",
            "explanation": "QuickSort degrades to O(n²) when the pivot is always the smallest or largest element.",
            "difficulty": 3
        },
        {
            "id": "cs_007", "topic": "Computer Science", "subtopic": "OS",
            "question": "What is the purpose of virtual memory?",
            "options": [
                "Extend available RAM using disk space",
                "Speed up CPU operations",
                "Improve network throughput",
                "Increase disk capacity"
            ],
            "correct": "Extend available RAM using disk space",
            "explanation": "Virtual memory uses disk (swap space) to extend the apparent RAM available.",
            "difficulty": 3
        },
        {
            "id": "cs_008", "topic": "Computer Science", "subtopic": "Databases",
            "question": "What does SQL stand for?",
            "options": [
                "Structured Query Language",
                "Standard Query Language",
                "Sequential Query Logic",
                "Simple Query Language"
            ],
            "correct": "Structured Query Language",
            "explanation": "SQL = Structured Query Language, used to interact with relational databases.",
            "difficulty": 1
        },
        {
            "id": "cs_009", "topic": "Computer Science", "subtopic": "ML/AI",
            "question": "What activation function outputs values between 0 and 1?",
            "options": ["Sigmoid", "ReLU", "Tanh", "Softmax"],
            "correct": "Sigmoid",
            "explanation": "Sigmoid σ(x) = 1/(1+e^-x) maps any value to (0,1).",
            "difficulty": 2
        },
        {
            "id": "cs_010", "topic": "Computer Science", "subtopic": "Recursion",
            "question": "What is the base case role in recursion?",
            "options": [
                "Stops infinite recursive calls",
                "Starts the recursion",
                "Allocates memory",
                "Handles exceptions"
            ],
            "correct": "Stops infinite recursive calls",
            "explanation": "The base case prevents infinite recursion by providing a termination condition.",
            "difficulty": 2
        },
        {
            "id": "cs_011", "topic": "Computer Science", "subtopic": "Networks",
            "question": "Which layer of the OSI model handles routing?",
            "options": ["Network Layer", "Data Link Layer", "Transport Layer", "Application Layer"],
            "correct": "Network Layer",
            "explanation": "Layer 3 (Network Layer) handles IP addressing and routing between networks.",
            "difficulty": 3
        },
        {
            "id": "cs_012", "topic": "Computer Science", "subtopic": "Security",
            "question": "What is a hash function property called when two different inputs produce the same output?",
            "options": ["Collision", "Avalanche", "Preimage", "Digest"],
            "correct": "Collision",
            "explanation": "A collision occurs when two different inputs produce the same hash output.",
            "difficulty": 3
        },
    ],
    "Chemistry": [
        {
            "id": "chem_001", "topic": "Chemistry", "subtopic": "Periodic Table",
            "question": "What is the atomic number of Carbon?",
            "options": ["6", "12", "14", "8"],
            "correct": "6",
            "explanation": "Carbon has 6 protons, giving it atomic number 6.",
            "difficulty": 1
        },
        {
            "id": "chem_002", "topic": "Chemistry", "subtopic": "Bonding",
            "question": "What type of bond forms between Na and Cl in table salt?",
            "options": ["Ionic", "Covalent", "Metallic", "Hydrogen"],
            "correct": "Ionic",
            "explanation": "Na donates an electron to Cl forming ionic bond (Na⁺ and Cl⁻).",
            "difficulty": 1
        },
        {
            "id": "chem_003", "topic": "Chemistry", "subtopic": "Organic",
            "question": "What functional group defines an alcohol?",
            "options": ["-OH", "-COOH", "-NH₂", "-CHO"],
            "correct": "-OH",
            "explanation": "Alcohols contain a hydroxyl group (-OH) bonded to a carbon atom.",
            "difficulty": 2
        },
        {
            "id": "chem_004", "topic": "Chemistry", "subtopic": "Reactions",
            "question": "In H₂ + ½O₂ → H₂O, what type of reaction is this?",
            "options": ["Synthesis (Combination)", "Decomposition", "Single Displacement", "Double Displacement"],
            "correct": "Synthesis (Combination)",
            "explanation": "Two reactants combine to form one product → synthesis reaction.",
            "difficulty": 2
        },
        {
            "id": "chem_005", "topic": "Chemistry", "subtopic": "Acid-Base",
            "question": "What is the pH of a neutral solution at 25°C?",
            "options": ["7", "0", "14", "5"],
            "correct": "7",
            "explanation": "Pure water at 25°C has [H⁺] = [OH⁻] = 10⁻⁷ M, so pH = 7.",
            "difficulty": 1
        },
        {
            "id": "chem_006", "topic": "Chemistry", "subtopic": "Thermodynamics",
            "question": "A reaction with ΔG < 0 is considered:",
            "options": ["Spontaneous", "Non-spontaneous", "At equilibrium", "Endothermic"],
            "correct": "Spontaneous",
            "explanation": "Negative ΔG (Gibbs free energy) indicates a spontaneous process.",
            "difficulty": 3
        },
        {
            "id": "chem_007", "topic": "Chemistry", "subtopic": "States of Matter",
            "question": "Which state of matter has definite volume but no definite shape?",
            "options": ["Liquid", "Solid", "Gas", "Plasma"],
            "correct": "Liquid",
            "explanation": "Liquids have fixed volume but take the shape of their container.",
            "difficulty": 1
        },
        {
            "id": "chem_008", "topic": "Chemistry", "subtopic": "Electrochemistry",
            "question": "In electrolysis, which electrode does oxidation occur at?",
            "options": ["Anode", "Cathode", "Both", "Neither"],
            "correct": "Anode",
            "explanation": "Oxidation (loss of electrons) occurs at the anode. 'AN OX' (anode oxidation).",
            "difficulty": 3
        },
        {
            "id": "chem_009", "topic": "Chemistry", "subtopic": "Gases",
            "question": "Boyle's Law states that pressure and volume are:",
            "options": ["Inversely proportional at constant T", "Directly proportional", "Equal", "Independent"],
            "correct": "Inversely proportional at constant T",
            "explanation": "PV = constant at constant temperature (Boyle's Law).",
            "difficulty": 2
        },
    ],
    "Biology": [
        {
            "id": "bio_001", "topic": "Biology", "subtopic": "Cell Biology",
            "question": "What is the powerhouse of the cell?",
            "options": ["Mitochondria", "Nucleus", "Ribosome", "Golgi apparatus"],
            "correct": "Mitochondria",
            "explanation": "Mitochondria produce ATP through cellular respiration.",
            "difficulty": 1
        },
        {
            "id": "bio_002", "topic": "Biology", "subtopic": "Genetics",
            "question": "DNA stands for:",
            "options": [
                "Deoxyribonucleic Acid",
                "Diribonucleic Acid",
                "Deoxyribonitric Acid",
                "Deoxyribinucleic Acid"
            ],
            "correct": "Deoxyribonucleic Acid",
            "explanation": "DNA = Deoxyribonucleic Acid, the molecule that carries genetic information.",
            "difficulty": 1
        },
        {
            "id": "bio_003", "topic": "Biology", "subtopic": "Evolution",
            "question": "Who proposed the theory of evolution by natural selection?",
            "options": ["Charles Darwin", "Gregor Mendel", "Louis Pasteur", "Isaac Newton"],
            "correct": "Charles Darwin",
            "explanation": "Darwin proposed natural selection in 'On the Origin of Species' (1859).",
            "difficulty": 1
        },
        {
            "id": "bio_004", "topic": "Biology", "subtopic": "Cell Division",
            "question": "What type of cell division produces gametes (sex cells)?",
            "options": ["Meiosis", "Mitosis", "Binary fission", "Budding"],
            "correct": "Meiosis",
            "explanation": "Meiosis produces haploid gametes (sperm and eggs) through two divisions.",
            "difficulty": 2
        },
        {
            "id": "bio_005", "topic": "Biology", "subtopic": "Photosynthesis",
            "question": "What is the primary pigment used in photosynthesis?",
            "options": ["Chlorophyll", "Haemoglobin", "Carotene", "Melanin"],
            "correct": "Chlorophyll",
            "explanation": "Chlorophyll absorbs sunlight energy to drive photosynthesis in plants.",
            "difficulty": 1
        },
        {
            "id": "bio_006", "topic": "Biology", "subtopic": "Proteins",
            "question": "What are the building blocks of proteins?",
            "options": ["Amino acids", "Nucleotides", "Fatty acids", "Monosaccharides"],
            "correct": "Amino acids",
            "explanation": "Proteins are polymers of amino acids linked by peptide bonds.",
            "difficulty": 1
        },
        {
            "id": "bio_007", "topic": "Biology", "subtopic": "Genetics",
            "question": "How many chromosomes do normal human somatic cells have?",
            "options": ["46", "23", "48", "44"],
            "correct": "46",
            "explanation": "Humans have 23 pairs (46) chromosomes in somatic (body) cells.",
            "difficulty": 1
        },
        {
            "id": "bio_008", "topic": "Biology", "subtopic": "Ecology",
            "question": "What is a food chain's ultimate energy source?",
            "options": ["The Sun", "Producers", "Decomposers", "Consumers"],
            "correct": "The Sun",
            "explanation": "Solar energy is captured by producers through photosynthesis.",
            "difficulty": 1
        },
        {
            "id": "bio_009", "topic": "Biology", "subtopic": "Homeostasis",
            "question": "What organ is primarily responsible for regulating blood glucose?",
            "options": ["Pancreas", "Liver", "Kidney", "Adrenal gland"],
            "correct": "Pancreas",
            "explanation": "The pancreas produces insulin and glucagon to regulate blood glucose.",
            "difficulty": 2
        },
        {
            "id": "bio_010", "topic": "Biology", "subtopic": "Immunology",
            "question": "What cells produce antibodies?",
            "options": ["B cells (plasma cells)", "T cells", "Red blood cells", "Natural killer cells"],
            "correct": "B cells (plasma cells)",
            "explanation": "B cells differentiate into plasma cells that produce specific antibodies.",
            "difficulty": 3
        },
    ]
}


def get_questions_for_topic(topic: str, n: int = 8, difficulty_target: int = 2) -> list:
    """Return n questions closest to target difficulty for a topic."""
    questions = QUESTION_BANK.get(topic, [])
    if not questions:
        return []
    # Sort by closeness to target difficulty
    questions = sorted(questions, key=lambda q: abs(q["difficulty"] - difficulty_target))
    return questions[:n]


def get_all_topics():
    return list(QUESTION_BANK.keys())


def get_topic_stats():
    return {topic: len(qs) for topic, qs in QUESTION_BANK.items()}
