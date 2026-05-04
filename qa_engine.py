from groq import Groq

# Groq client setup
client = Groq(
    api_key="KEY"
)


def generate_answer(question, relevant_chunks):
    """
    Advanced research-paper Q&A engine.

    Features:
    ✔ Main-body only answers
    ✔ Strong hallucination control
    ✔ Page-aware citations
    ✔ Better category/task/model distinction
    ✔ Bullet-point optimized formatting
    ✔ Structured academic responses
    ✔ Higher factual precision
    ✔ Portfolio-grade performance
    """

    # ----------------------------
    # PAGE-AWARE CONTEXT BUILDING
    # ----------------------------
    formatted_chunks = []

    for chunk_data in relevant_chunks:
        formatted_chunks.append(
            f"[Page {chunk_data['page']}]\n{chunk_data['text']}"
        )

    context = "\n\n".join(formatted_chunks[:8])

    # ----------------------------
    # ADVANCED PROMPT
    # ----------------------------
    prompt = f"""
You are an elite AI research paper assistant.

MISSION:
Answer the user's question with maximum factual accuracy using ONLY the provided research paper context.

STRICT RULES:
- Use ONLY the provided research paper content.
- Use ONLY the MAIN BODY of the paper.
- Ignore:
    * references
    * bibliography
    * citations
    * author names
    * footnotes
    * acknowledgements
    * publisher/license metadata
    * unrelated metadata
  unless directly relevant.
- Do NOT use outside knowledge.
- Do NOT speculate.
- Do NOT hallucinate.
- Do NOT infer unsupported claims.
- Do NOT fabricate missing details.
- Prefer highly factual, concise, evidence-based answers.

FOCUS PRIORITIES:
- section titles
- formal classifications
- explicit definitions
- learning paradigms
- methodologies
- algorithms
- model architectures
- datasets
- benchmarks
- limitations
- conclusions
- reproducibility

IMPORTANT ANALYTICAL DISTINCTIONS:
- Distinguish clearly between:
    * learning paradigms
    * tasks
    * algorithms
    * models
    * datasets
    * applications
- NEVER confuse:
    * classification/regression tasks
    with
    * supervised/unsupervised/reinforcement paradigms
- Prefer formal classifications over isolated examples.
- Prefer section headings over scattered mentions.
- Avoid duplicate concepts or repeated items.

QUESTION TYPE HANDLING:

If question asks about:
1. Categories / Types / Kinds / Paradigms:
   → Return ONLY major learning paradigms explicitly discussed.

2. Algorithms / Methods / Techniques:
   → Return ONLY explicitly named algorithms or techniques.

3. Models / Systems / Architectures:
   → Return ONLY explicit model families or systems.

4. Datasets / Benchmarks / Examples:
   → Return ONLY named datasets, benchmarks, or case studies.

5. Limitations / Challenges / Weaknesses:
   → Return ONLY directly discussed limitations.

6. Conclusions / Findings:
   → Return explicit findings only.

7. Practical Applications:
   → Return ONLY explicitly stated applications.
   → Never speculate real-world domains.

OUTPUT FORMATTING RULES:
- Use clear section headings whenever useful.
- Prefer bullet points for lists.
- Use numbered lists for structured explanations.
- Keep formatting clean and highly readable.
- Avoid dense long paragraphs.
- Be academically professional.
- Be highly specific.
- Mention page citations whenever directly supported.
- Example:
  "MNIST dataset is explicitly discussed (Page 4)."
- If multiple pages support the answer, include all relevant pages.
- If evidence is partial, clearly mention uncertainty.

🔥 IMPORTANT RULE:
- If definitions are NOT explicitly provided in the paper,
  DO NOT generate textbook-style definitions.
- Instead say:
  "The paper discusses these paradigms as major machine learning categories."

- If answer is absent, reply EXACTLY:
"The paper does not explicitly mention this."

QUALITY CONTROL:
Before answering:
- Check for unsupported assumptions
- Remove duplicate points
- Ensure classification accuracy
- Ensure answer matches question type
- Ensure evidence comes from provided context only

Research Paper Context:
{context}

User Question:
{question}

Generate the best possible answer with:
- Clear headings
- Bullet points
- Numbered lists where useful
- Page citations
- Concise factual precision
- Professional academic structure
"""

    # ----------------------------
    # MODEL RESPONSE
    # ----------------------------
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.05
    )

    return response.choices[0].message.content.strip()