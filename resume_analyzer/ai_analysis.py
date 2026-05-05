"""Local AI-style resume analysis without external APIs."""

import math
import re
from collections import Counter

from .analysis import extract_job_keywords


RESUME_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in",
    "into", "is", "it", "of", "on", "or", "that", "the", "their", "this",
    "to", "with", "work", "worked", "using", "use", "used",
}

IMPACT_TERMS = {
    "automated", "built", "delivered", "designed", "developed", "improved",
    "increased", "launched", "optimized", "reduced", "scaled", "streamlined",
}


def analyze_resume_with_local_ai(text, job_description="", base_analysis=None):
    """Return local NLP insights that behave like an AI review layer."""
    sentences = split_sentences(text)
    job_keywords = extract_job_keywords(job_description)
    resume_terms = weighted_terms(text)
    job_terms = weighted_terms(job_description)
    similarity = cosine_similarity(resume_terms, job_terms) if job_description else 0

    matched_keywords = [
        keyword for keyword in job_keywords
        if keyword.lower() in text.lower()
    ]
    missing_keywords = [
        keyword for keyword in job_keywords
        if keyword.lower() not in text.lower()
    ]

    strengths = infer_strengths(text, sentences, matched_keywords, base_analysis)
    concerns = infer_concerns(text, missing_keywords, base_analysis)
    actions = build_priority_actions(concerns, missing_keywords)

    return {
        "enabled": True,
        "engine": "Local NLP AI",
        "summary": build_ai_summary(similarity, matched_keywords, missing_keywords, base_analysis),
        "fit_score": calculate_fit_score(similarity, matched_keywords, missing_keywords, base_analysis),
        "career_level": infer_career_level(text),
        "strengths": strengths,
        "concerns": concerns,
        "priority_actions": actions,
        "rewritten_summary": rewrite_summary(text, matched_keywords, base_analysis),
        "evidence": extract_evidence(sentences),
    }


def split_sentences(text):
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [sentence.strip(" -\t") for sentence in sentences if sentence.strip()]


def tokenize(text):
    return [
        token for token in re.findall(r"[a-z][a-z0-9+#.-]{2,}", text.lower())
        if token not in RESUME_STOPWORDS
    ]


def weighted_terms(text):
    tokens = tokenize(text)
    counts = Counter(tokens)
    total = max(1, sum(counts.values()))
    return {term: count / total for term, count in counts.items()}


def cosine_similarity(left, right):
    common = set(left) & set(right)
    numerator = sum(left[token] * right[token] for token in common)
    left_norm = math.sqrt(sum(weight * weight for weight in left.values()))
    right_norm = math.sqrt(sum(weight * weight for weight in right.values()))
    if not left_norm or not right_norm:
        return 0
    return numerator / (left_norm * right_norm)


def calculate_fit_score(similarity, matched_keywords, missing_keywords, base_analysis):
    keyword_total = len(matched_keywords) + len(missing_keywords)
    keyword_ratio = len(matched_keywords) / keyword_total if keyword_total else 0
    base_score = (base_analysis or {}).get("score", 0) / 100
    score = (similarity * 35) + (keyword_ratio * 40) + (base_score * 25)
    return round(min(100, max(0, score)))


def infer_strengths(text, sentences, matched_keywords, base_analysis):
    strengths = []
    lower_text = text.lower()

    if matched_keywords:
        strengths.append(f"Matches important role terms such as {', '.join(matched_keywords[:5])}.")

    if any(term in lower_text for term in IMPACT_TERMS):
        strengths.append("Uses achievement-focused language that signals ownership.")

    if re.search(r"\d+%|\d+\+|\d+\s+(users|projects|clients|reports|teams)", lower_text):
        strengths.append("Includes measurable results, which makes impact easier to trust.")

    if base_analysis and len(base_analysis.get("sections_found", [])) >= 4:
        strengths.append("Has a recognizable resume structure for ATS parsing.")

    if not strengths and sentences:
        strengths.append("Provides enough text for a first-pass AI review.")

    return strengths[:4]


def infer_concerns(text, missing_keywords, base_analysis):
    concerns = []
    word_count = len(re.findall(r"\b[\w+#.-]+\b", text))

    if missing_keywords:
        concerns.append(f"Missing target terms: {', '.join(missing_keywords[:6])}.")

    if word_count < 250:
        concerns.append("Resume is short, so the AI has limited evidence to evaluate.")

    if base_analysis and base_analysis.get("sections_missing"):
        missing = ", ".join(base_analysis["sections_missing"][:4])
        concerns.append(f"Missing common sections: {missing}.")

    if not re.search(r"\d+%|\d+\+|\d+\s+(users|projects|clients|reports|teams)", text.lower()):
        concerns.append("Achievements need more numbers or concrete scale.")

    return concerns[:4]


def build_priority_actions(concerns, missing_keywords):
    actions = []

    if missing_keywords:
        actions.append(f"Add truthful examples for {', '.join(missing_keywords[:4])}.")

    if any("numbers" in concern or "scale" in concern for concern in concerns):
        actions.append("Rewrite top bullets with metrics, scope, and outcome.")

    if any("sections" in concern for concern in concerns):
        actions.append("Add clear Summary, Skills, Experience, Education, and Projects headings.")

    if not actions:
        actions.append("Tailor the summary and first three bullets to the target job.")

    return actions[:4]


def infer_career_level(text):
    lower_text = text.lower()
    if any(term in lower_text for term in ["led", "managed", "architected", "mentored", "principal", "senior"]):
        return "Senior or leadership leaning"
    if any(term in lower_text for term in ["intern", "trainee", "fresher", "student"]):
        return "Entry level"
    return "Early to mid level"


def build_ai_summary(similarity, matched_keywords, missing_keywords, base_analysis):
    grade = (base_analysis or {}).get("grade", "reviewable")
    if matched_keywords:
        focus = f"matches {len(matched_keywords)} target keyword(s)"
    else:
        focus = "needs clearer role-specific keywords"

    if missing_keywords:
        gap = f"has {len(missing_keywords)} keyword gap(s)"
    else:
        gap = "has no major keyword gaps from the supplied role"

    if similarity >= 0.25:
        alignment = "strong alignment"
    elif similarity >= 0.12:
        alignment = "moderate alignment"
    else:
        alignment = "limited alignment"

    return f"The resume is {grade.lower()}, shows {alignment}, {focus}, and {gap}."


def rewrite_summary(text, matched_keywords, base_analysis):
    skills = (base_analysis or {}).get("skills", [])
    focus_terms = matched_keywords[:3] or skills[:3]
    focus_text = ", ".join(focus_terms) if focus_terms else "role-relevant tools"
    level = infer_career_level(text).lower()
    return (
        f"{level.capitalize()} candidate with hands-on experience in {focus_text}, "
        "focused on building measurable, business-ready results."
    )


def extract_evidence(sentences):
    scored = []
    for sentence in sentences:
        score = 0
        score += 2 if re.search(r"\d+%|\d+\+|\d+\s+(users|projects|clients|reports|teams)", sentence.lower()) else 0
        score += 1 if any(term in sentence.lower() for term in IMPACT_TERMS) else 0
        if score:
            scored.append((score, sentence))

    return [sentence for _, sentence in sorted(scored, reverse=True)[:3]]
