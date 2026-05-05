"""Shared analyzer vocabulary and scoring constants."""

SKILL_CATEGORIES = {
    "Programming": [
        "python", "java", "javascript", "typescript", "c", "c++", "c#", "go",
        "php", "ruby", "kotlin", "swift", "sql", "html", "css",
    ],
    "Frameworks": [
        "flask", "django", "fastapi", "spring", "spring boot", "react",
        "angular", "vue", "node.js", "express", "bootstrap", "tailwind",
    ],
    "Data & AI": [
        "machine learning", "deep learning", "artificial intelligence", "nlp",
        "data analysis", "data science", "pandas", "numpy", "scikit-learn",
        "tensorflow", "pytorch", "power bi", "tableau", "excel",
    ],
    "Databases": [
        "mysql", "postgresql", "mongodb", "sqlite", "oracle", "redis",
        "firebase", "nosql",
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes", "git", "github",
        "ci/cd", "linux", "jenkins",
    ],
    "Core CS": [
        "data structures", "algorithms", "oop", "object oriented programming",
        "api", "rest api", "microservices", "system design",
    ],
    "Professional": [
        "communication", "leadership", "teamwork", "problem solving",
        "collaboration", "project management", "analytical thinking",
    ],
}

ALL_SKILLS = sorted({skill for skills in SKILL_CATEGORIES.values() for skill in skills})

ACTION_VERBS = {
    "achieved", "automated", "built", "created", "delivered", "designed",
    "developed", "improved", "increased", "launched", "led", "managed",
    "optimized", "reduced", "resolved", "scaled", "streamlined",
}

SECTION_ALIASES = {
    "Summary": ["summary", "profile", "objective", "career objective"],
    "Skills": ["skills", "technical skills", "core competencies"],
    "Experience": ["experience", "work experience", "employment", "internship"],
    "Education": ["education", "academic background", "qualification"],
    "Projects": ["projects", "academic projects", "personal projects"],
    "Certifications": ["certifications", "certificates", "licenses"],
}

STOPWORDS = {
    "and", "the", "for", "with", "that", "this", "from", "your", "you",
    "are", "will", "our", "has", "have", "job", "role", "work", "team",
    "using", "use", "into", "their", "they", "candidate", "experience",
    "skills", "ability", "knowledge", "responsibilities", "requirements",
}
