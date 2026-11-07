"""
AI-Powered Student Assistant Chatbot
Using Generative AI, Google Gemini API, Streamlit, and FAISS.
"""

import os
import io
import warnings
from dotenv import load_dotenv
import streamlit as st
from rag_engine import RAGEngine

warnings.filterwarnings("ignore", category=FutureWarning)
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Student Assistant Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS matching the project report screenshots
st.markdown("""
<style>
    /* Global font & background adjustments */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar Styling - Deep Blue */
    [data-testid="stSidebar"] {
        background-color: #1e50bb !important;
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        color: #ffffff !important;
        font-weight: 500;
        font-size: 15px;
    }

    /* Style sidebar radio buttons to look like navigation pills */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
        background: transparent;
        padding: 8px 16px;
        border-radius: 20px;
        margin-bottom: 6px;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
    }

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-checked="true"],
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) {
        background-color: #ffffff !important;
        color: #1e50bb !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) * {
        color: #1e50bb !important;
        font-weight: 600 !important;
    }

    /* Header Banner - Deep Green */
    .banner-card {
        background: #145a32;
        color: #ffffff;
        padding: 24px 28px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(20, 90, 50, 0.15);
    }
    .banner-title {
        font-size: 24px;
        font-weight: 700;
        margin: 0 0 8px 0;
        display: flex;
        align-items: center;
        gap: 10px;
        color: #ffffff;
    }
    .banner-subtitle {
        font-size: 14px;
        font-weight: 400;
        margin: 0;
        color: #d4efdf;
    }

    /* Section Subheaders */
    .section-header {
        font-size: 18px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Upload Box - Light Bordered Card */
    .upload-card {
        border: 2px dashed #cbd5e1;
        background-color: #f8fafc;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Chat Messages */
    .user-bubble {
        background-color: #d96b43;
        color: #ffffff;
        padding: 14px 20px;
        border-radius: 12px;
        margin-bottom: 16px;
        font-size: 15px;
        font-weight: 500;
        line-height: 1.5;
        box-shadow: 0 2px 6px rgba(217, 107, 67, 0.2);
    }

    .answer-bubble {
        background-color: #eafaf1;
        border: 1.5px solid #27ae60;
        color: #1e4620;
        padding: 16px 20px;
        border-radius: 12px;
        margin-bottom: 16px;
        font-size: 15px;
        line-height: 1.6;
        box-shadow: 0 2px 6px rgba(39, 174, 96, 0.1);
    }

    /* Source Citation Card - Warm Yellow/Gold */
    .source-card {
        background-color: #fef9e7;
        border: 1.5px solid #f9e79f;
        border-radius: 12px;
        padding: 16px 20px;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .source-header {
        font-size: 14px;
        font-weight: 600;
        color: #7d6608;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .source-highlight {
        background-color: #ffe066;
        color: #212529;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 14.5px;
        line-height: 1.6;
        display: inline-block;
    }

    /* Category Buttons styling */
    .category-chip {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 16px;
        font-size: 13px;
        font-weight: 600;
        margin-right: 8px;
        border: 1px solid rgba(0,0,0,0.08);
    }
    .chip-subjects { background-color: #fef9c3; color: #854d0e; }
    .chip-assignments { background-color: #e0f2fe; color: #0369a1; }
    .chip-exams { background-color: #ffedd5; color: #c2410c; }

    /* Upload pill in sidebar */
    .doc-pill {
        background-color: rgba(255, 255, 255, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 13px;
        margin: 12px 0;
        display: flex;
        align-items: center;
        gap: 6px;
        word-break: break-all;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session State
if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = RAGEngine()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_doc_name" not in st.session_state:
    st.session_state.uploaded_doc_name = None

if "preset_question" not in st.session_state:
    st.session_state.preset_question = ""


# Sidebar
with st.sidebar:
    st.markdown("### 🎓 Student Assistant")
    
    # Document indicator
    if st.session_state.uploaded_doc_name:
        st.markdown(f'<div class="doc-pill">📄 {st.session_state.uploaded_doc_name}</div>', unsafe_allow_html=True)
    
    # Navigation menu
    page = st.radio(
        label="Navigation",
        options=["Home", "Chat history", "About"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # API Key Configuration
    st.markdown("##### ⚙️ Gemini Configuration")
    user_api_key = st.text_input(
        "Google Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        placeholder="AIzaSy...",
        help="Paste your Google Gemini API key to enable live LLM generation."
    )
    if user_api_key:
        st.session_state.rag_engine.set_api_key(user_api_key)
        st.caption("✅ Gemini API Active")
    else:
        st.caption("ℹ️ Running in Smart Fallback Mode")

    # Sample Document Loader Button
    sample_pdf_path = os.path.join(os.path.dirname(__file__), "sample_docs", "unit3_notes.pdf")
    if os.path.exists(sample_pdf_path):
        if st.button("📑 Load Demo (unit3_notes.pdf)", use_container_width=True):
            with open(sample_pdf_path, "rb") as f:
                content = f.read()
            st.session_state.rag_engine.build_vector_store(io.BytesIO(content), "unit3_notes.pdf")
            st.session_state.uploaded_doc_name = "unit3_notes.pdf"
            st.success("Loaded unit3_notes.pdf successfully!")
            st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()


# Page Routing
if page == "Home":
    # Green Banner
    st.markdown("""
    <div class="banner-card">
        <div class="banner-title">
            <span>🤖</span> AI-Powered Student Assistant Chatbot
        </div>
        <div class="banner-subtitle">
            Ask academic questions and clear your doubts using Generative AI and Gemini
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Document Upload Section
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown("**📁 Upload study material (optional)**")
    uploaded_file = st.file_uploader(
        "Upload PDF Document",
        type=["pdf"],
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        if st.session_state.uploaded_doc_name != uploaded_file.name:
            with st.spinner(f"Extracting text & building FAISS vector index for {uploaded_file.name}..."):
                chunk_count = st.session_state.rag_engine.build_vector_store(uploaded_file, uploaded_file.name)
                st.session_state.uploaded_doc_name = uploaded_file.name
                st.success(f"Successfully processed {uploaded_file.name} ({chunk_count} passages indexed in FAISS).")

    # Question Input
    query_val = st.session_state.preset_question if st.session_state.preset_question else ""
    user_query = st.text_input(
        "Ask your question here",
        value=query_val,
        placeholder="Ask your question here",
        label_visibility="collapsed"
    )

    # Reset preset question after populating input
    if st.session_state.preset_question:
        st.session_state.preset_question = ""

    # Category Chips
    col1, col2, col3, col_fill = st.columns([1.2, 1.4, 1.2, 4])
    with col1:
        if st.button("🏷️ Subjects", use_container_width=True):
            st.session_state.preset_question = "What is Retrieval-Augmented Generation (RAG)?"
            st.rerun()
    with col2:
        if st.button("📝 Assignments", use_container_width=True):
            st.session_state.preset_question = "Why is RAG used in academic assistants?"
            st.rerun()
    with col3:
        if st.button("🎯 Exams", use_container_width=True):
            st.session_state.preset_question = "Explain Transformer Self-Attention in NLP."
            st.rerun()

    # Submit Button
    ask_clicked = st.button("Submit Question", type="primary")

    if (ask_clicked or user_query) and user_query.strip():
        # Check if already processed
        if not st.session_state.chat_history or st.session_state.chat_history[-1]["question"] != user_query.strip():
            with st.spinner("Retrieving knowledge and generating answer..."):
                response = st.session_state.rag_engine.query(user_query.strip())
                st.session_state.chat_history.append({
                    "question": user_query.strip(),
                    "answer": response["answer"],
                    "source_file": response.get("source_file"),
                    "source_page": response.get("source_page"),
                    "highlighted_passage": response.get("highlighted_passage")
                })

    # Display the latest conversation below
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown('<div class="section-header">💬 Ask your doubts</div>', unsafe_allow_html=True)
        latest = st.session_state.chat_history[-1]

        # User Bubble (Terracotta Orange)
        st.markdown(f'<div class="user-bubble">{latest["question"]}</div>', unsafe_allow_html=True)

        # Chatbot Answer Bubble (Mint Green)
        st.markdown(f'<div class="answer-bubble">{latest["answer"]}</div>', unsafe_allow_html=True)

        # Source Citation with Highlighted Page (Ivory/Gold)
        if latest.get("source_file") and latest.get("source_page"):
            passage_html = ""
            if latest.get("highlighted_passage"):
                passage_html = f'<div class="source-highlight">{latest["highlighted_passage"]}</div>'
            st.markdown(f"""
            <div class="source-card">
                <div class="source-header">📄 Source: {latest["source_file"]}, page {latest["source_page"]}</div>
                {passage_html}
            </div>
            """, unsafe_allow_html=True)

        # Follow-up Input Box
        follow_up = st.text_input(
            "Ask a follow-up question",
            placeholder="Ask a follow-up question",
            key="follow_up_input",
            label_visibility="collapsed"
        )
        if st.button("Send Follow-up") and follow_up.strip():
            with st.spinner("Processing follow-up..."):
                resp = st.session_state.rag_engine.query(follow_up.strip())
                st.session_state.chat_history.append({
                    "question": follow_up.strip(),
                    "answer": resp["answer"],
                    "source_file": resp.get("source_file"),
                    "source_page": resp.get("source_page"),
                    "highlighted_passage": resp.get("highlighted_passage")
                })
                st.rerun()


elif page == "Chat history":
    st.markdown('<div class="section-header">💬 Ask your doubts</div>', unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.info("No queries asked yet. Return to the Home tab to ask questions or upload study material.")
    else:
        for idx, item in enumerate(st.session_state.chat_history):
            # User Bubble
            st.markdown(f'<div class="user-bubble">{item["question"]}</div>', unsafe_allow_html=True)

            # Answer Bubble
            st.markdown(f'<div class="answer-bubble">{item["answer"]}</div>', unsafe_allow_html=True)

            # Source Box
            if item.get("source_file") and item.get("source_page"):
                passage_html = ""
                if item.get("highlighted_passage"):
                    passage_html = f'<div class="source-highlight">{item["highlighted_passage"]}</div>'
                st.markdown(f"""
                <div class="source-card">
                    <div class="source-header">📄 Source: {item["source_file"]}, page {item["source_page"]}</div>
                    {passage_html}
                </div>
                """, unsafe_allow_html=True)

        # Follow-up input at bottom of chat history (Fig. 2)
        follow_up_hist = st.text_input(
            "Ask a follow-up question",
            placeholder="Ask a follow-up question",
            key="follow_up_history_input",
            label_visibility="collapsed"
        )
        if st.button("Send Follow-up", key="btn_hist_followup") and follow_up_hist.strip():
            with st.spinner("Processing follow-up..."):
                resp = st.session_state.rag_engine.query(follow_up_hist.strip())
                st.session_state.chat_history.append({
                    "question": follow_up_hist.strip(),
                    "answer": resp["answer"],
                    "source_file": resp.get("source_file"),
                    "source_page": resp.get("source_page"),
                    "highlighted_passage": resp.get("highlighted_passage")
                })
                st.rerun()


elif page == "About":
    st.markdown("## 📖 About This Mini Project")
    st.markdown("""
    ### AI-Powered Student Assistant Chatbot Using Generative AI

    The **AI-Powered Student Assistant Chatbot** is an intelligent academic application designed to help students ask coursework questions and receive context-grounded answers in natural language.

    ---

    ### 🔑 Key Pillars of the System

    1. **Generative AI & Large Language Models (LLMs)**
       - Powered by the **Google Gemini API** (`gemini-1.5-flash`), delivering fast, contextual, and accurate reasoning.
    
    2. **Retrieval-Augmented Generation (RAG)**
       - Extends the model's capabilities with real-time academic documents (syllabi, lecture notes, textbook chapters).
       - Prevents hallucinations and guarantees factual grounding.

    3. **Semantic Vector Search (FAISS)**
       - Uses **Facebook AI Similarity Search (FAISS)** to index high-dimensional embeddings of study materials.
       - Rapidly retrieves the most relevant passages based on cosine similarity.

    4. **Source Attribution & Verification**
       - Identifies the exact document and page number for every retrieved answer.
       - Highlights the verbatim passage with transparent provenance, as demonstrated in Chapter 7 of the project report.

    5. **Web Application Development**
       - Built with **Python** and **Streamlit**, featuring custom responsive UI styling matching academic design standards.
    """)