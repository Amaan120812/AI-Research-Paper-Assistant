# ============================
# FILE: embeddings.py
# ============================

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re


# ----------------------------
# MODEL SETUP
# ----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")


# ----------------------------
# QUALITY FILTERS
# ----------------------------
IGNORE_PATTERNS = [
    "references",
    "bibliography",
    "copyright",
    "license",
    "publisher",
    "doi",
    "issn",
    "volume",
    "issue",
    "author",
    "et al"
]


def is_low_quality_chunk(chunk_text):
    """
    Weak/noisy chunk detect karega.
    """

    chunk_lower = chunk_text.lower()

    # Too short
    if len(chunk_text) < 120:
        return True

    # Too long
    if len(chunk_text) > 5000:
        return True

    # Metadata heavy
    if any(pattern in chunk_lower for pattern in IGNORE_PATTERNS):
        return True

    # Too numeric
    digit_ratio = sum(c.isdigit() for c in chunk_text) / max(len(chunk_text), 1)

    if digit_ratio > 0.35:
        return True

    # Must contain language
    if not re.search(r"[A-Za-z]", chunk_text):
        return True

    return False


# ----------------------------
# QUESTION TYPE DETECTION
# ----------------------------
def detect_question_focus(question):
    """
    User query ka intent detect karega.
    """

    q = question.lower()

    if any(word in q for word in [
        "type", "types", "category",
        "categories", "kind",
        "paradigm"
    ]):
        return "categories"

    elif any(word in q for word in [
        "algorithm", "algorithms",
        "method", "methods",
        "model", "models"
    ]):
        return "algorithms"

    elif any(word in q for word in [
        "dataset", "datasets",
        "benchmark", "data",
        "mnist", "example"
    ]):
        return "datasets"

    elif any(word in q for word in [
        "limitation", "limitations",
        "weakness", "challenge"
    ]):
        return "limitations"

    return "general"


# ----------------------------
# KEYWORD BOOSTING
# ----------------------------
def calculate_keyword_boost(chunk_text, focus_type):
    """
    Specific question types ke liye semantic keyword boost.
    """

    chunk_lower = chunk_text.lower()

    keyword_map = {
        "categories": [
            "supervised",
            "unsupervised",
            "semi-supervised",
            "reinforcement"
        ],

        "algorithms": [
            "svm",
            "support vector",
            "decision tree",
            "bayesian",
            "naive bayes",
            "regression",
            "neural network"
        ],

        "datasets": [
            "mnist",
            "dataset",
            "benchmark",
            "ocr",
            "training data"
        ],

        "limitations": [
            "limitation",
            "limitations",
            "challenge",
            "constraint",
            "weakness"
        ]
    }

    boost = 0.0

    if focus_type in keyword_map:
        for keyword in keyword_map[focus_type]:
            if keyword in chunk_lower:
                boost += 0.15

    return boost


# ----------------------------
# EMBEDDING GENERATION
# ----------------------------
def create_embeddings(chunks):
    """
    Page-aware chunks ke semantic embeddings generate karega.

    Input:
    [
        {
            "text": "...",
            "page": 3
        }
    ]
    """

    # Extract only text for embedding model
    chunk_texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        chunk_texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings


# ----------------------------
# MAIN RETRIEVAL
# ----------------------------
def retrieve_relevant_chunks(question, chunks, embeddings, top_k=8):
    """
    Advanced semantic retrieval:

    ✔ Page-aware
    ✔ Question-aware
    ✔ Duplicate reduction
    ✔ Metadata filtering
    ✔ Better factual precision
    ✔ Research-grade retrieval
    """

    # Encode question
    question_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # Similarity
    similarities = cosine_similarity(
        question_embedding,
        embeddings
    )[0]

    # Detect query type
    focus_type = detect_question_focus(question)

    ranked_results = []

    for idx, chunk_data in enumerate(chunks):

        chunk_text = chunk_data["text"]

        # Skip weak chunks
        if is_low_quality_chunk(chunk_text):
            continue

        score = similarities[idx]

        # Semantic boost
        score += calculate_keyword_boost(
            chunk_text,
            focus_type
        )

        ranked_results.append(
            (
                idx,
                score
            )
        )

    # Sort descending
    ranked_results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    relevant_chunks = []
    seen_chunks = set()

    for idx, score in ranked_results:

        chunk_text = chunks[idx]["text"]
        page = chunks[idx]["page"]

        # Deduplicate
        signature = chunk_text[:250]

        if signature in seen_chunks:
            continue

        seen_chunks.add(signature)

        relevant_chunks.append({
            "text": chunk_text,
            "page": page,
            "score": round(float(score), 4)
        })

        if len(relevant_chunks) >= top_k:
            break

    return relevant_chunks