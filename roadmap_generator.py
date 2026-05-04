# ============================
# FILE: roadmap_generator.py
# ============================

from groq import Groq

# Groq client setup
client = Groq(
    api_key="KEY"
)


def generate_roadmap(full_text):
    """
    Full research paper ka highly structured, source-grounded roadmap generate karega.

    Features:
    ✔ Exact paper-only analysis
    ✔ Strong hallucination reduction
    ✔ Better academic structure
    ✔ Accurate categories
    ✔ Cleaner formatting
    ✔ No speculative practical applications
    ✔ Portfolio/demo quality
    """

    # Token-safe truncation
    limited_text = full_text[:15000]

    prompt = f"""
You are an expert AI research paper roadmap generator.

TASK:
Analyze ONLY the uploaded research paper and generate a structured reading roadmap.

STRICT RULES:
- Use ONLY exact content from the provided paper
- Ignore:
    * references
    * bibliography
    * citations
    * author affiliations
    * publisher metadata
    * copyright/license text
- No external assumptions
- No outside knowledge
- No generic ML explanations unless directly supported
- No speculative practical applications unless explicitly stated in the paper
- Do NOT infer real-world domains unless directly mentioned
- Prioritize:
    * section titles
    * formal classifications
    * explicit categories
    * algorithms
    * datasets
    * benchmarks
    * methodology
    * results
    * limitations
    * conclusions
- Distinguish clearly between:
    * learning categories
    * tasks
    * algorithms
    * datasets
    * model families
- Do NOT confuse:
    * classification/regression tasks
    with
    * core learning categories
- Prefer formal paper classifications over examples
- Avoid duplicate items
- Beginner-friendly language
- Concise explanations
- Clean markdown formatting
- Use bullet points where helpful
- Keep answers factual and source-grounded

RETURN FORMAT EXACTLY:

# Research Paper Reading Roadmap

## 1. Problem Statement & Main Goal
- Main research problem
- Primary objective
- Why it matters

## 2. Core Concepts / Learning Categories
- Explicitly defined learning paradigms
- Major theoretical categories
- Why important

## 3. Methodology / Algorithms Covered
- Specific algorithms
- Techniques
- Formal methods
- Why important

## 4. Datasets / Benchmarks / Examples
- Named datasets
- Benchmarks
- Practical examples directly mentioned
- Why important

## 5. Models / Systems Explained
- Architectures
- Systems
- Model families
- Why important

## 6. Key Findings / Results
- Explicit findings
- Performance insights
- Why important

## 7. Limitations / Weaknesses
- Directly mentioned limitations
- Missing depth
- Constraints
- Why important

## 8. Conclusion
- Main takeaway
- Final summary
- Why important

## 9. Practical Use / Reproducibility
- ONLY explicitly stated applications
- Educational value
- Implementation/reproducibility if directly discussed
- If absent, clearly state:
  "The paper does not explicitly mention this."

IMPORTANT:
- If any section lacks sufficient evidence, explicitly say:
"The paper does not explicitly mention this."
- Never fabricate missing sections.

Research Paper:
{limited_text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()