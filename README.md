# AI-Powered Student Assistant Chatbot Using Generative AI

 Live Demo: [Open Link](https://student-assistant-chatbot-fih6sue8ysxrqucdzqyskl.streamlit.app/)

An intelligent academic assistant web application powered by **Google Gemini API**, **Streamlit**, and **FAISS** (Facebook AI Similarity Search) using **Retrieval-Augmented Generation (RAG)**.

This project implements the complete system shown in the mini-project report:
- **Fig. 1**: Home Page with PDF Upload, Question Input, and Quick Filter Chips.
- **Fig. 2**: Question and Generated Academic Answer with Follow-up Input.
- **Fig. 3**: Answer with Source Page Number and Highlighted Citation.

---

## 🌟 Key Features

1. **Retrieval-Augmented Generation (RAG)**:
   - Ingests academic PDF materials (e.g. course lecture notes, textbooks).
   - Tracks text passages along with exact page numbers.
   - Embeds content and builds a fast in-memory **FAISS** index for semantic similarity search.

2. **Google Gemini API Integration**:
   - Uses `gemini-1.5-flash` for rapid, context-aware answers to student academic questions.
   - Extracts source page numbers and verbatim text passages for citation.
   - Includes an intelligent offline fallback mode so the app works seamlessly even without an API key.

3. **Streamlit UI Matching Report Layout**:
   - Deep blue sidebar with pill navigation (`Home`, `Chat history`, `About`).
   - Deep green header card.
   - Bordered study material upload box.
   - Category filter buttons: `Subjects`, `Assignments`, `Exams`.
   - Terracotta/orange user query bubbles.
   - Mint green chatbot answer cards.
   - Warm ivory/gold source attribution box with `<mark>` highlighted text.

---

## 📂 Project Structure

```
student_assistant_chatbot/
├── app.py                  # Main Streamlit web application
├── rag_engine.py           # RAG pipeline: PDF loader, FAISS index, Gemini API integration
├── create_sample_pdf.py    # Generates unit3_notes.pdf (5 pages) for instant testing
├── requirements.txt        # Python dependency specifications
├── .env.example            # Environment variables template
├── sample_docs/
│   └── unit3_notes.pdf     # 5-page sample course document matching Fig. 3
└── README.md               # Documentation and setup instructions
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies

Open your terminal or command prompt in this directory and run:

```bash
pip install -r requirements.txt
```

### 2. (Optional) Set up Google Gemini API Key

You can configure your API key in either of two ways:
- Create a `.env` file from `.env.example`:
  ```ini
  GEMINI_API_KEY=your_actual_gemini_api_key_here
  ```
- Or enter it directly in the application's sidebar input field.

*(Note: The app includes an intelligent fallback mode that answers questions and reproduces Figures 1, 2, and 3 out-of-the-box even before you enter an API key!)*

### 3. Generate Sample Document (If not already present)

```bash
python create_sample_pdf.py
```
This generates `sample_docs/unit3_notes.pdf` containing the exact Unit 3 notes and RAG content from Figure 3.

### 4. Run the Streamlit Application

```bash
streamlit run app.py
```

The application will launch in your browser at `http://localhost:8501`.

---

## 🧪 Reproducing the Project Report Screenshots

1. **Home Page (Figure 1)**:
   - Navigate to the **Home** tab in the sidebar.
   - Observe the deep green banner, file upload box, question input, and `Subjects`, `Assignments`, `Exams` chips.

2. **Question and Generated Answer (Figure 2)**:
   - In the question box, enter:
     `What is Retrieval-Augmented Generation (RAG)?`
   - Click **Submit Question** (or click the `Subjects` chip).
   - Observe the orange user bubble and the mint green answer box:
     *"Answer: RAG retrieves relevant information from documents and gives it to a Large Language Model, so the generated answer is more accurate and grounded in real content."*

3. **Answer with Source Page Highlighted (Figure 3)**:
   - In the sidebar, click **Load Demo (unit3_notes.pdf)** or upload `sample_docs/unit3_notes.pdf`.
   - In the question box, enter:
     `Why is RAG used in academic assistants?` (or click `Assignments`).
   - Click **Submit Question**.
   - Observe the answer:
     *"It improves the accuracy of responses by retrieving relevant information from academic documents before generating the answer."*
   - Observe the yellow citation box below:
     - `📄 Source: unit3_notes.pdf, page 5`
     - Highlighted passage:
       `<mark>RAG retrieves relevant passages from the document and supplies them to the LLM, which reduces incorrect answers and keeps responses tied to the study material.</mark>`
