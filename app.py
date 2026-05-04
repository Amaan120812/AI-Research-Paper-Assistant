# ============================
# FILE: app.py
# ============================

import streamlit as st
from pdf_processor import extract_text_from_pdf
from roadmap_generator import generate_roadmap
from chunking import create_chunks
from embeddings import create_embeddings, retrieve_relevant_chunks
from qa_engine import generate_answer


# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="AI Research Paper Assistant",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ----------------------------
# CUSTOM CSS
# ----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.main {
    background: linear-gradient(135deg, #0b1020, #111827);
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1550px;
}

/* HERO */
.hero-title {
    font-size: 3.3rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0.5rem;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: #cbd5e1;
    margin-bottom: 2rem;
}

/* METRICS */
.metric-card {
    background: rgba(255,255,255,0.05);
    padding: 1.5rem;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
}

.metric-value {
    font-size: 2rem;
    font-weight: bold;
    color: white;
}

.metric-label {
    color: #94a3b8;
    font-size: 1rem;
}

/* ROADMAP CARDS */
.roadmap-card {
    background: #f8fafc;
    color: #111827;
    padding: 1.7rem;
    border-radius: 22px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.14);
    margin-bottom: 1.5rem;
    min-height: 340px;
    transition: transform 0.2s ease;
}

.roadmap-card:hover {
    transform: translateY(-4px);
}

.roadmap-title {
    font-size: 1.35rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
    color: #111827;
}

.roadmap-text {
    color: #334155;
    line-height: 1.75;
    font-size: 1rem;
    white-space: pre-wrap;
}

/* ANSWER BOX */
.answer-box {
    background: #052e16;
    padding: 1.7rem;
    border-radius: 18px;
    border-left: 6px solid #22c55e;
    color: white;
    margin-top: 1rem;
}

/* SOURCE BOX */
.source-box {
    background: rgba(255,255,255,0.05);
    padding: 0.8rem 1rem;
    border-radius: 12px;
    margin-top: 1rem;
    color: #cbd5e1;
    font-size: 0.95rem;
}

/* HEADINGS */
.section-heading {
    font-size: 2rem;
    font-weight: 700;
    margin-top: 2rem;
    margin-bottom: 1rem;
    color: white;
}

/* QUESTION SECTION */
.question-container {
    background: rgba(255,255,255,0.04);
    padding: 1.5rem;
    border-radius: 18px;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ----------------------------
# HEADER
# ----------------------------
st.markdown(
    '<div class="hero-title">📘 AI Research Paper Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">Upload any research paper PDF, generate a premium AI-powered roadmap, and ask highly accurate source-grounded questions instantly.</div>',
    unsafe_allow_html=True
)


# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.header("📂 Upload PDF")
    uploaded_file = st.file_uploader(
        "Choose a research paper PDF",
        type=["pdf"]
    )


# ----------------------------
# MAIN PROCESSING
# ----------------------------
if uploaded_file:

    with st.spinner("🔍 Processing research paper, building semantic knowledge base, and generating roadmap..."):

        # PDF Processing
        pdf_data = extract_text_from_pdf(uploaded_file)

        title = pdf_data["title"]
        full_text = pdf_data["full_text"]
        pages = pdf_data["pages"]

        # Chunking with page support
        chunks = create_chunks(
            full_text,
            total_pages=len(pages)
        )

        # Embeddings
        embeddings = create_embeddings(chunks)

        # Roadmap
        roadmap = generate_roadmap(full_text)

    st.success("✅ Research paper processed successfully!")

    # ----------------------------
    # TITLE DISPLAY
    # ----------------------------
    st.markdown(f"# 📄 {title}")

    # ----------------------------
    # METRICS
    # ----------------------------
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{len(pages)}</div>
            <div class="metric-label">Pages</div>
        </div>
        ''', unsafe_allow_html=True)

    with c2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{len(chunks)}</div>
            <div class="metric-label">Semantic Chunks</div>
        </div>
        ''', unsafe_allow_html=True)

    with c3:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-value">Ready</div>
            <div class="metric-label">AI Knowledge Base</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")


    # ----------------------------
    # ROADMAP SECTION
    # ----------------------------
    st.markdown(
        '<div class="section-heading">🗺️ Research Paper Reading Roadmap</div>',
        unsafe_allow_html=True
    )

    st.caption("Structured paper understanding, optimized for learning and analysis.")

    sections = [s.strip() for s in roadmap.split("##") if s.strip()]

    for i in range(0, len(sections), 2):

        cols = st.columns(2)

        for j in range(2):

            if i + j < len(sections):

                sec = sections[i + j]

                lines = sec.split("\n")

                sec_title = lines[0].strip()

                sec_body = "\n".join(lines[1:]).strip()

                with cols[j]:
                    st.markdown(f'''
                    <div class="roadmap-card">
                        <div class="roadmap-title">{sec_title}</div>
                        <div class="roadmap-text">{sec_body}</div>
                    </div>
                    ''', unsafe_allow_html=True)

    st.markdown("---")


    # ----------------------------
    # PDF PREVIEW
    # ----------------------------
    with st.expander("📖 Full PDF Extract Preview"):
        st.text_area(
            "Extracted Paper Content",
            full_text[:12000],
            height=450
        )

    st.markdown("---")


    # ----------------------------
    # Q&A SECTION
    # ----------------------------
    st.markdown(
        '<div class="section-heading">❓ Ask Questions About This Paper</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="question-container">', unsafe_allow_html=True)

    user_question = st.text_input(
        "Enter your research question:"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    if user_question:

        with st.spinner("🧠 Retrieving relevant sections and generating answer..."):

            relevant_chunks = retrieve_relevant_chunks(
                user_question,
                chunks,
                embeddings,
                top_k=8
            )

            answer = generate_answer(
                user_question,
                relevant_chunks
            )

        # ----------------------------
        # ANSWER DISPLAY
        # ----------------------------
        st.markdown(f'''
        <div class="answer-box">
            <h3>📌 AI Answer</h3>
            <p>{answer}</p>
        </div>
        ''', unsafe_allow_html=True)

        # ----------------------------
        # SOURCE CITATIONS
        # ----------------------------
        source_pages = sorted(
            list(set(chunk["page"] for chunk in relevant_chunks))
        )

        st.markdown(f'''
        <div class="source-box">
            📚 <strong>Source Pages:</strong> {", ".join(map(str, source_pages))}
        </div>
        ''', unsafe_allow_html=True)

        # ----------------------------
        # RETRIEVED CHUNKS
        # ----------------------------
        with st.expander("🔍 Relevant Retrieved Research Sections"):

            for idx, chunk_data in enumerate(relevant_chunks):

                st.markdown(
                    f"### Chunk {idx+1} (Page {chunk_data['page']})"
                )

                st.write(chunk_data["text"])

                st.markdown("---")

else:
    st.info("📂 Upload a research paper PDF from the sidebar to begin.")