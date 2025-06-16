#frontend
import streamlit as st
from flashcard_generator import FlashcardGenerator
from utils.exporter import Exporter
import os
import time

# --- Page Config ---
st.set_page_config(
    page_title="AI Flashcard Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS with Hover Effect ---
st.markdown("""
<style>
    :root {
        --primary: #4a8cff;
        --primary-hover: #3a7aee;
        --card-bg: #f8fafc;
        --text: #1e293b;
        --border: #e2e8f0;
    }
    
    [data-theme="dark"] {
        --primary: #60a5fa;
        --primary-hover: #4a8cff;
        --card-bg: #1e293b;
        --text: #f8fafc;
        --border: #334155;
    }
    
    .flashcard {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    .flashcard:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    
    .flashcard-question {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 1rem;
    }
    
    .flashcard-answer {
        font-size: 1rem;
        color: var(--text);
        padding: 1rem;
        background: rgba(74, 140, 255, 0.1);
        border-radius: 8px;
        border-left: 3px solid var(--primary);
    }
    
    .difficulty-tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .easy { background: #ecfdf5; color: #059669; }
    .medium { background: #eff6ff; color: #2563eb; }
    .hard { background: #fef2f2; color: #dc2626; }
    
    [data-testid="stExpander"] {
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
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

# Initialize session state
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = None

# --- Sidebar ---
with st.sidebar:
    st.title("ℹ️ Instructions")
    st.markdown("""
    1. **Input** your study material
    2. Set optional parameters
    3. Click **Generate Flashcards**
    4. **Review** and **export** your cards
    """)
    st.markdown("---")
    
    if st.button("🧹 Clear Session", type="secondary", use_container_width=True):
        st.session_state.flashcards = None
        st.rerun()

# --- Main UI ---
st.title("🧠 AI Flashcard Generator")
st.markdown("Transform any content into study flashcards")

# --- Input Section ---
input_method = st.radio(
    "Input Method:",
    ["Text Input", "File Upload"],
    horizontal=True
)

if input_method == "Text Input":
    content = st.text_area(
        "Paste your study material here", 
        height=250,
        placeholder="Lecture notes, textbook content, or any study material..."
    )
else:
    content = st.file_uploader(
        "Upload PDF or TXT", 
        type=["pdf", "txt"],
        help="Supported formats: PDF or plain text"
    )

subject = st.text_input("Subject (Optional)", placeholder="e.g. Biology, History")
difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"], index=1)

# --- Generation Button ---
if st.button("✨ Generate Flashcards", type="primary", use_container_width=True):
    if content:
        with st.spinner(f"Generating {difficulty.lower()} flashcards..."):
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
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please provide some content first")

# --- Display Flashcards ---
if st.session_state.flashcards:
    st.subheader(f"Generated Flashcards ({difficulty})")
    
    # Two-column layout
    cols = st.columns(2)
    for i, card in enumerate(st.session_state.flashcards):
        with cols[i % 2]:
            with st.expander(f"Card {i+1}: {card['question'][:50]}...", expanded=True):
                st.markdown(f"""
                <div class='flashcard'>
                    <div class='difficulty-tag {card.get('difficulty', 'medium').lower()}'>{card.get('difficulty', difficulty)}</div>
                    <div class='flashcard-question'>❓ {card['question']}</div>
                    <div class='flashcard-answer'><strong>Answer:</strong> {card['answer']}</div>
                </div>
                """, unsafe_allow_html=True)

    # --- Export Options ---
    st.subheader("Export Options")
    export_cols = st.columns(3)  # Changed from 4 to 3 columns since we removed Print button
    
    with export_cols[0]:
        csv = Exporter.to_csv_string(st.session_state.flashcards)
        st.download_button(
            "📝 CSV",
            data=csv,
            file_name=f"flashcards_{subject or 'general'}_{difficulty.lower()}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with export_cols[1]:
        json_data = Exporter.to_json_string(st.session_state.flashcards)
        st.download_button(
            "📋 JSON",
            data=json_data,
            file_name=f"flashcards_{subject or 'general'}_{difficulty.lower()}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with export_cols[2]:
        anki = Exporter.to_anki_string(st.session_state.flashcards)
        st.download_button(
            "🃏 Anki",
            data=anki,
            file_name=f"flashcards_{subject or 'general'}_{difficulty.lower()}.txt",
            mime="text/plain",
            use_container_width=True
        )

# Footer
st.markdown("---")
st.caption("© 2023 AI Flashcard Generator | Powered by Google Gemini")