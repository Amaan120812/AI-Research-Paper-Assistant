# ============================
# FILE: pdf_processor.py
# ============================

import fitz  # PyMuPDF
import re


# Keywords to ignore in title extraction
IGNORE_KEYWORDS = [
    "copyright",
    "license",
    "publisher",
    "open-access",
    "open access",
    "issn",
    "doi",
    "journal",
    "volume",
    "issue",
    "received",
    "accepted",
    "available online",
    "corresponding author",
    "email",
    "www.",
    "http",
    "https"
]


def clean_text(text):
    """
    General text cleanup.
    """
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_valid_title_candidate(text):
    """
    Check if line/block title candidate ho sakta hai.
    """

    if not text:
        return False

    text_lower = text.lower()

    # Ignore bad keywords
    if any(keyword in text_lower for keyword in IGNORE_KEYWORDS):
        return False

    # Too short
    if len(text) < 15:
        return False

    # Too long (likely paragraph)
    if len(text) > 300:
        return False

    # Ignore mostly numeric
    digit_ratio = sum(c.isdigit() for c in text) / max(len(text), 1)
    if digit_ratio > 0.3:
        return False

    # Must contain letters
    if not re.search(r"[A-Za-z]", text):
        return False

    return True


def extract_title_from_first_page(doc):
    """
    Advanced title extraction:
    ✔ Largest font priority
    ✔ Multi-line title merge
    ✔ Metadata filtering
    ✔ Better professional title detection
    """

    first_page = doc[0]
    blocks = first_page.get_text("dict")["blocks"]

    candidates = []

    for block in blocks:
        if "lines" not in block:
            continue

        block_text_parts = []
        max_font_size = 0

        for line in block["lines"]:
            line_text_parts = []

            for span in line["spans"]:
                span_text = clean_text(span["text"])

                if not span_text:
                    continue

                line_text_parts.append(span_text)
                max_font_size = max(max_font_size, span["size"])

            if line_text_parts:
                block_text_parts.append(" ".join(line_text_parts))

        if not block_text_parts:
            continue

        combined_text = clean_text(" ".join(block_text_parts))

        if is_valid_title_candidate(combined_text):
            candidates.append({
                "text": combined_text,
                "font_size": max_font_size,
                "length_score": len(combined_text)
            })

    # Sort by:
    # 1. Largest font
    # 2. Reasonable title length
    candidates.sort(
        key=lambda x: (
            x["font_size"],
            -abs(x["length_score"] - 120)  # prefer moderate title length
        ),
        reverse=True
    )

    if candidates:
        return candidates[0]["text"]

    return "Untitled Research Paper"


def extract_text_from_pdf(pdf_file):
    """
    PDF se:
    ✔ Accurate title
    ✔ Full clean text
    ✔ Page-wise structured content
    ✔ Better metadata filtering

    Returns:
    {
        title,
        full_text,
        pages
    }
    """

    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")

    full_text = ""
    pages = []

    # Professional title extraction
    title = extract_title_from_first_page(doc)

    # Full paper extraction
    for page_num, page in enumerate(doc):
        raw_text = page.get_text()

        cleaned_page_text = clean_text(raw_text)

        full_text += cleaned_page_text + "\n\n"

        pages.append({
            "page_number": page_num + 1,
            "text": cleaned_page_text
        })

    return {
        "title": title,
        "full_text": full_text.strip(),
        "pages": pages
    }