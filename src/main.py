import streamlit as st
from flashcard_generator import FlashcardGenerator
from utils.exporter import Exporter
import os

# --- Page Config ---
st.set_page_config(
    page_title="AI Flashcard Generator 🧠",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>

    :root {
        --primary: #4a8cff;
        --primary-hover: #3a7aee;
        --card-bg: #1e293b;
        --text: #f8fafc;
        --border: #334155;
    }

    .flashcard {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid var(--border);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
    }

    .flashcard:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
    }

    .flashcard-question {
        font-size: 1.2rem;
        font-weight: 750;
        color: var(--text);
        margin-bottom: 1rem;
    }

    .flashcard-answer {
        font-size: 1rem;
        color: var(--text);
        background: rgba(74, 140, 255, 0.1);
        border-left: 4px solid var(--primary);
        border-radius: 10px;
        padding: 1rem;
        margin-top: 0.5rem;
    }

    .difficulty-tag {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    .easy { background: #d1fae5; color: #065f46; }
    .medium { background: #dbeafe; color: #1e40af; }
    .hard { background: #fee2e2; color: #991b1b; }

    [data-testid="stExpander"] {
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }

    button {
        background: var(--primary) !important;
        border: none !important;
    }

    button:hover {
        background: var(--primary-hover) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize session ---
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = None

# --- Sidebar ---
with st.sidebar:
    st.title("📋 How to Use")
    st.markdown("""
    1. ✍️ **Input** your material  
    2. 🎛️ Set parameters  
    3. ✨ Click **Generate Flashcards**  
    4. 👀 **Review** & 💾 **Download**  
    """)
    st.markdown("---")
    
    if st.button("🧹 Clear Session", type="secondary", use_container_width=True):
        st.session_state.flashcards = None
        st.rerun()

# --- Main UI ---
st.title("🧠 AI Flashcard Generator")
st.markdown("🚀 Instantly transform your content into interactive study flashcards")

# --- Input Section ---
input_method = st.radio(
    "Choose Input Method:",
    ["Text Input", "File Upload"],
    horizontal=True
)

if input_method == "Text Input":
    content = st.text_area(
        "📄 Paste your material here:", 
        height=300,
        placeholder="Lecture notes, textbook content, or any study material..."
    )
else:
    content = st.file_uploader(
        "📂 Upload PDF or TXT file", 
        type=["pdf", "txt"],
        help="Supported formats: PDF or plain text"
    )

subject = st.text_input("📚 Subject (optional)", placeholder="e.g. Biology, History, AI")
difficulty = st.selectbox("🎓 Difficulty Level", ["Easy", "Medium", "Hard"], index=1)

# --- Generate Button ---
if st.button("✨ Generate Flashcards", type="primary", use_container_width=True):
    if content:
        with st.spinner(f"✨ Generating {difficulty.lower()} flashcards..."):
            try:
                generator = FlashcardGenerator()

                if input_method == "Text Input":
                    flashcards = generator.process_text(content, subject, difficulty)
                else:
                    temp_path = os.path.join("/tmp", content.name)
                    with open(temp_path, "wb") as f:
                        content.seek(0)
                        f.write(content.read())
                    flashcards = generator.process_file(temp_path, subject, difficulty)
                    os.remove(temp_path)

                st.session_state.flashcards = flashcards
                st.success(f"✅ Generated {len(flashcards)} {difficulty.lower()} flashcards!")

            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")
    else:
        st.warning("⚠️ Please provide some content first!")

# --- Display Flashcards ---
if st.session_state.flashcards:
    st.subheader(f"📋 Generated Flashcards ({difficulty})")

    cols = st.columns(2)
    for i, card in enumerate(st.session_state.flashcards):
        with cols[i % 2]:
            with st.expander(f"Card {i+1}: {card['question']}"):
                st.markdown(f"""
                <div class='flashcard'>
                    <div class='difficulty-tag {card.get('difficulty', 'medium').lower()}'>{card.get('difficulty', difficulty)}</div>
                    <div class='flashcard-answer'><strong>Answer:</strong> {card['answer']}</div>
                </div>
                """, unsafe_allow_html=True)

    # --- Export Section ---
    st.subheader("📦 Export Your Flashcards")
    export_cols = st.columns(2)

    with export_cols[0]:
        csv = Exporter.to_csv_string(st.session_state.flashcards)
        st.download_button(
            "📝 Export as CSV",
            data=csv,
            file_name=f"flashcards_{subject or 'general'}_{difficulty.lower()}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with export_cols[1]:
        json_data = Exporter.to_json_string(st.session_state.flashcards)
        st.download_button(
            "📋 Export as JSON",
            data=json_data,
            file_name=f"flashcards_{subject or 'general'}_{difficulty.lower()}.json",
            mime="application/json",
            use_container_width=True
        )

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align:center; color: #888; font-size: 0.9rem;">
    © 2025 <strong>Flashcard Generator</strong> | Powered by <strong>Google Gemini</strong>
</div>
""", unsafe_allow_html=True)