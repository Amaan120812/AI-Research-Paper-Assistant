# ============================
# FILE: chunking.py
# ============================

import re


def clean_text(text):
    """
    Basic PDF text cleanup:
    ✔ Extra spaces removed
    ✔ Broken formatting fixed
    ✔ Cleaner retrieval quality
    """

    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


def estimate_page_number(start_index, full_length, total_pages):
    """
    Approximate page mapping based on text position.
    Useful when exact PDF page segmentation is unavailable.
    """

    if total_pages <= 0:
        return 1

    relative_position = start_index / max(full_length, 1)

    estimated_page = int(relative_position * total_pages) + 1

    return min(max(estimated_page, 1), total_pages)


def create_chunks(text, chunk_size=1000, overlap=200, total_pages=1):
    """
    Research paper text ko smarter overlapping semantic chunks me divide karega.

    Features:
    ✔ Cleaner chunks
    ✔ Better semantic continuity
    ✔ Page-aware metadata
    ✔ Improved retrieval precision
    ✔ Citation support
    ✔ Reduced noise
    ✔ Better portfolio quality

    Returns:
    [
        {
            "text": chunk_text,
            "page": estimated_page_number
        }
    ]
    """

    # Clean text first
    text = clean_text(text)

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        # Sentence boundary protection
        if end < text_length:

            sentence_break = text.rfind(".", start, end)

            if sentence_break != -1 and sentence_break > start + 300:
                end = sentence_break + 1

        chunk = text[start:end].strip()

        # Skip weak chunks
        if len(chunk) > 150:

            page_number = estimate_page_number(
                start,
                text_length,
                total_pages
            )

            chunks.append({
                "text": chunk,
                "page": page_number
            })

        # Move with overlap
        start += chunk_size - overlap

    return chunks