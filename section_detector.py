import re

SECTION_KEYWORDS = [
    "abstract",
    "introduction",
    "background",
    "methodology",
    "methods",
    "architecture",
    "dataset",
    "experiments",
    "results",
    "evaluation",
    "discussion",
    "limitations",
    "future work",
    "conclusion",
    "related work"
]


def detect_sections(pages_data):
    detected_sections = []

    for page_data in pages_data:
        page_num = page_data["page"]
        text = page_data["text"]

        lines = text.split("\n")

        for line in lines:
            clean_line = line.strip().lower()

            for keyword in SECTION_KEYWORDS:
                if keyword in clean_line:
                    detected_sections.append({
                        "section": keyword.title(),
                        "page": page_num,
                        "content": text[:2000]
                    })
                    break

    # Remove duplicate sections
    unique_sections = []
    seen = set()

    for sec in detected_sections:
        if sec["section"] not in seen:
            unique_sections.append(sec)
            seen.add(sec["section"])

    return unique_sections