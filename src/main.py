# #frontend
# import streamlit as st
# from flashcard_generator import FlashcardGenerator
# from utils.exporter import Exporter
# import os
# import time

# # --- Page Config ---
# st.set_page_config(
#     page_title="AI Flashcard Generator",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # --- Custom CSS with Hover Effect ---
# st.markdown("""
# <style>
#     :root {
#         --primary: #4a8cff;
#         --primary-hover: #3a7aee;
#         --card-bg: #1e293b;
#         --text: #f8fafc;;
#         --border: #e2e8f0;
#     }
    
#     [data-theme="dark"] {
#         --primary: #60a5fa;
#         --primary-hover: #4a8cff;
#         --card-bg: #1e293b;
#         --text: #f8fafc;
#         --border: #334155;
#     }
    
#     .flashcard {
#         background: var(--card-bg);
#         border-radius: 12px;
#         padding: 1.5rem;
#         margin: 1rem 0;
#         border: 1px solid var(--border);
#         box-shadow: 0 4px 6px rgba(0,0,0,0.05);
#         transition: all 0.2s ease;
#     }
    
#     .flashcard:hover {
#         transform: translateY(-3px);
#         box-shadow: 0 6px 12px rgba(0,0,0,0.1);
#     }
    
#     .flashcard-question {
#         font-size: 1.2rem;
#         font-weight: 600;
#         color: var(--text);
#         margin-bottom: 1rem;
#     }
    
#     .flashcard-answer {
#         font-size: 1rem;
#         color: var(--text);
#         padding: 1rem;
#         background: rgba(74, 140, 255, 0.1);
#         border-radius: 8px;
#         border-left: 3px solid var(--primary);
#     }
    
#     .difficulty-tag {
#         display: inline-block;
#         padding: 0.25rem 0.75rem;
#         border-radius: 1rem;
#         font-size: 0.8rem;
#         font-weight: 600;
#         margin-bottom: 0.5rem;
#     }
    
#     .easy { background: #ecfdf5; color: #059669; }
#     .medium { background: #eff6ff; color: #2563eb; }
#     .hard { background: #fef2f2; color: #dc2626; }
    
#     [data-testid="stExpander"] {
#         border: 1px solid var(--border) !important;
#         border-radius: 10px !important;
#     }
    
#     button {
#         background: var(--primary) !important;
#         border: none !important;
#     }
    
#     button:hover {
#         background: var(--primary-hover) !important;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Initialize session state
# if 'flashcards' not in st.session_state:
#     st.session_state.flashcards = None

# # --- Sidebar ---
# with st.sidebar:
#     st.title("ℹ️ Instructions")
#     st.markdown("""
#     1. **Input** your study material
#     2. Set optional parameters
#     3. Click **Generate Flashcards**
#     4. **Review** and **export** your cards
#     """)
#     st.markdown("---")
    
#     if st.button("🧹 Clear Session", type="secondary", use_container_width=True):
#         st.session_state.flashcards = None
#         st.rerun()

# # --- Main UI ---
# st.title("🧠 AI Flashcard Generator")
# st.markdown("Transform any content into study flashcards")

# # --- Input Section ---
# input_method = st.radio(
#     "Input Method:",
#     ["Text Input", "File Upload"],
#     horizontal=True
# )

# if input_method == "Text Input":
#     content = st.text_area(
#         "Paste your study material here", 
#         height=250,
#         placeholder="Lecture notes, textbook content, or any study material..."
#     )
# else:
#     content = st.file_uploader(
#         "Upload PDF or TXT", 
#         type=["pdf", "txt"],
#         help="Supported formats: PDF or plain text"
#     )

# subject = st.text_input("Subject (Optional)", placeholder="e.g. Biology, History")
# difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"], index=1)

# # --- Generation Button ---
# if st.button("✨ Generate Flashcards", type="primary", use_container_width=True):
#     if content:
#         with st.spinner(f"Generating {difficulty.lower()} flashcards..."):
#             try:
#                 generator = FlashcardGenerator()
                
#                 if input_method == "Text Input":
#                     flashcards = generator.process_text(content, subject, difficulty)
#                 else:
#                     temp_path = os.path.join("/tmp", content.name)
#                     with open(temp_path, "wb") as f:
#                         content.seek(0)
#                         f.write(content.read())
#                     flashcards = generator.process_file(temp_path, subject, difficulty)
#                     os.remove(temp_path)
                
#                 st.session_state.flashcards = flashcards
#                 st.success(f"✅ Generated {len(flashcards)} {difficulty.lower()} flashcards!")
                
#             except Exception as e:
#                 st.error(f"Error: {str(e)}")
#     else:
#         st.warning("Please provide some content first")

# # --- Display Flashcards ---
# if st.session_state.flashcards:
#     st.subheader(f"Generated Flashcards ({difficulty})")
    
#     # Two-column layout
#     cols = st.columns(2)
#     for i, card in enumerate(st.session_state.flashcards):
#         with cols[i % 2]:
#             with st.expander(f"Card {i+1}: {card['question'][:50]}...", expanded=True):
#                 st.markdown(f"""
#                 <div class='flashcard'>
#                     <div class='difficulty-tag {card.get('difficulty', 'medium').lower()}'>{card.get('difficulty', difficulty)}</div>
#                     <div class='flashcard-question'>❓ {card['question']}</div>
#                     <div class='flashcard-answer'><strong>Answer:</strong> {card['answer']}</div>
#                 </div>
#                 """, unsafe_allow_html=True)

#     # --- Export Options ---
#     st.subheader("Export Options")
#     export_cols = st.columns(3)  # Changed from 4 to 3 columns since we removed Print button
    
#     with export_cols[0]:
#         csv = Exporter.to_csv_string(st.session_state.flashcards)
#         st.download_button(
#             "📝 CSV",
#             data=csv,
#             file_name=f"flashcards_{subject or 'general'}_{difficulty.lower()}.csv",
#             mime="text/csv",
#             use_container_width=True
#         )
    
#     with export_cols[1]:
#         json_data = Exporter.to_json_string(st.session_state.flashcards)
#         st.download_button(
#             "📋 JSON",
#             data=json_data,
#             file_name=f"flashcards_{subject or 'general'}_{difficulty.lower()}.json",
#             mime="application/json",
#             use_container_width=True
#         )
    
#     with export_cols[2]:
#         anki = Exporter.to_anki_string(st.session_state.flashcards)
#         st.download_button(
#             "🃏 Anki",
#             data=anki,
#             file_name=f"flashcards_{subject or 'general'}_{difficulty.lower()}.txt",
#             mime="text/plain",
#             use_container_width=True
#         )

# # Footer
# st.markdown("---") 
# st.caption("© 2023 AI Flashcard Generator | Powered by Google Gemini")


# import streamlit as st
# from flashcard_generator import FlashcardGenerator
# from utils.exporter import Exporter
# import os
# import time
# import random

# # --- Page Config ---
# st.set_page_config(
#     page_title="AI Flashcard Generator Pro",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # --- Enhanced Custom CSS with Animations ---
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
#     * {
#         font-family: 'Inter', sans-serif;
#     }
    
#     :root {
#         --primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         --primary-solid: #667eea;
#         --secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
#         --success: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
#         --warning: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
#         --card-bg: rgba(255, 255, 255, 0.9);
#         --card-dark: rgba(30, 41, 59, 0.9);
#         --text: #1e293b;
#         --text-light: #64748b;
#         --border: rgba(226, 232, 240, 0.3);
#         --shadow: 0 10px 25px rgba(0,0,0,0.08);
#         --shadow-hover: 0 20px 40px rgba(0,0,0,0.12);
#         --bg-light: rgba(248, 250, 252, 0.6);
#         --bg-dark: rgba(15, 23, 42, 0.8);
#     }
    
#     .main-header {
#         text-align: center;
#         padding: 2rem 0;
#         background: var(--primary);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#         font-size: 3rem;
#         font-weight: 700;
#         margin-bottom: 1rem;
#         animation: fadeInUp 0.8s ease-out;
#     }
    
#     .subtitle {
#         text-align: center;
#         color: var(--text-light);
#         font-size: 1.2rem;
#         margin-bottom: 3rem;
#         animation: fadeInUp 0.8s ease-out 0.2s both;
#     }
    
#     @keyframes fadeInUp {
#         from {
#             opacity: 0;
#             transform: translateY(30px);
#         }
#         to {
#             opacity: 1;
#             transform: translateY(0);
#         }
#     }
    
#     @keyframes pulse {
#         0%, 100% { transform: scale(1); }
#         50% { transform: scale(1.05); }
#     }
    
#     @keyframes slideIn {
#         from {
#             opacity: 0;
#             transform: translateX(-20px);
#         }
#         to {
#             opacity: 1;
#             transform: translateX(0);
#         }
#     }
    
#     .input-container {
#         background: rgba(248, 250, 252, 0.8);
#         border-radius: 20px;
#         padding: 2rem;
#         margin: 2rem 0;
#         box-shadow: var(--shadow);
#         border: none;
#         animation: slideIn 0.6s ease-out;
#         transition: all 0.3s ease;
#         backdrop-filter: blur(10px);
#     }
    
#     .input-container:hover {
#         box-shadow: var(--shadow-hover);
#         transform: translateY(-2px);
#     }
    
#     .flashcard-modern {
#         background: rgba(255, 255, 255, 0.9);
#         border-radius: 20px;
#         padding: 2rem;
#         margin: 1rem 0;
#         box-shadow: var(--shadow);
#         border: none;
#         transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
#         position: relative;
#         overflow: hidden;
#         animation: slideIn 0.6s ease-out;
#         backdrop-filter: blur(10px);
#     }
    
#     .flashcard-modern::before {
#         content: '';
#         position: absolute;
#         top: 0;
#         left: 0;
#         right: 0;
#         height: 4px;
#         background: var(--primary);
#         transform: scaleX(0);
#         transition: transform 0.3s ease;
#     }
    
#     .flashcard-modern:hover {
#         transform: translateY(-8px) rotate(1deg);
#         box-shadow: var(--shadow-hover);
#     }
    
#     .flashcard-modern:hover::before {
#         transform: scaleX(1);
#     }
    
#     .question-text {
#         font-size: 1.3rem;
#         font-weight: 600;
#         color: var(--text);
#         margin-bottom: 1.5rem;
#         line-height: 1.6;
#         display: flex;
#         align-items: center;
#         gap: 0.5rem;
#     }
    
#     .answer-text {
#         background: rgba(248, 250, 252, 0.8);
#         border-radius: 12px;
#         padding: 1.5rem;
#         font-size: 1.1rem;
#         line-height: 1.7;
#         border-left: 4px solid var(--primary-solid);
#         position: relative;
#         margin-top: 1rem;
#         backdrop-filter: blur(5px);
#     }
    
#     .difficulty-badge {
#         display: inline-flex;
#         align-items: center;
#         gap: 0.5rem;
#         padding: 0.5rem 1rem;
#         border-radius: 50px;
#         font-size: 0.85rem;
#         font-weight: 600;
#         text-transform: uppercase;
#         letter-spacing: 0.5px;
#         margin-bottom: 1rem;
#         animation: pulse 2s infinite;
#     }
    
#     .easy { 
#         background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
#         color: #059669;
#         box-shadow: 0 4px 12px rgba(5, 150, 105, 0.2);
#     }
    
#     .medium { 
#         background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
#         color: #2563eb;
#         box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
#     }
    
#     .hard { 
#         background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
#         color: #dc2626;
#         box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
#     }
    
#     .stats-container {
#         display: grid;
#         grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
#         gap: 1rem;
#         margin: 2rem 0;
#     }
    
#     .stat-card {
#         background: rgba(255, 255, 255, 0.9);
#         border-radius: 16px;
#         padding: 1.5rem;
#         text-align: center;
#         box-shadow: var(--shadow);
#         border: none;
#         transition: all 0.3s ease;
#         backdrop-filter: blur(10px);
#     }
    
#     .stat-card:hover {
#         transform: translateY(-4px);
#         box-shadow: var(--shadow-hover);
#     }
    
#     .stat-number {
#         font-size: 2.5rem;
#         font-weight: 700;
#         background: var(--primary);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#     }
    
#     .stat-label {
#         color: var(--text-light);
#         font-size: 0.9rem;
#         text-transform: uppercase;
#         letter-spacing: 0.5px;
#         margin-top: 0.5rem;
#     }
    
#     .export-grid {
#         display: grid;
#         grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
#         gap: 1rem;
#         margin: 2rem 0;
#     }
    
#     .export-button {
#         background: var(--primary);
#         border: none;
#         border-radius: 12px;
#         padding: 1rem;
#         color: white;
#         font-weight: 600;
#         font-size: 1rem;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         gap: 0.5rem;
#         text-decoration: none;
#     }
    
#     .export-button:hover {
#         transform: translateY(-2px);
#         box-shadow: var(--shadow-hover);
#     }
    
#     .progress-container {
#         background: #f1f5f9;
#         border-radius: 10px;
#         height: 8px;
#         margin: 1rem 0;
#         overflow: hidden;
#     }
    
#     .progress-bar {
#         height: 100%;
#         background: var(--primary);
#         border-radius: 10px;
#         transition: width 0.5s ease;
#         animation: shimmer 2s infinite;
#     }
    
#     @keyframes shimmer {
#         0% { background-position: -200px 0; }
#         100% { background-position: 200px 0; }
#     }
    
#     .floating-elements {
#         position: fixed;
#         top: 0;
#         left: 0;
#         width: 100%;
#         height: 100%;
#         pointer-events: none;
#         z-index: -1;
#     }
    
#     .floating-shape {
#         position: absolute;
#         background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
#         border-radius: 50%;
#         animation: float 6s ease-in-out infinite;
#     }
    
#     @keyframes float {
#         0%, 100% { transform: translateY(0px); }
#         50% { transform: translateY(-20px); }
#     }
    
#     /* Hide Streamlit elements */
#     [data-testid="InputInstructions"] { display: none; }
#     .reportview-container .main .block-container { padding-top: 2rem; }
#     header[data-testid="stHeader"] { display: none; }
    
#     /* Custom button styles */
#     .stButton > button {
#         background: var(--primary) !important;
#         border: none !important;
#         border-radius: 12px !important;
#         padding: 0.75rem 2rem !important;
#         font-weight: 600 !important;
#         transition: all 0.3s ease !important;
#         color: white !important;
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-2px) !important;
#         box-shadow: var(--shadow-hover) !important;
#     }
    
#     /* Enhanced sidebar */
#     .css-1d391kg {
#         background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
#     }
    
#     /* Text area and input styling */
#     .stTextArea > div > div > textarea {
#         border-radius: 12px !important;
#         border: 2px solid var(--border) !important;
#         transition: all 0.3s ease !important;
#     }
    
#     .stTextArea > div > div > textarea:focus {
#         border-color: var(--primary-solid) !important;
#         box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Add floating background elements
# st.markdown("""
# <div class="floating-elements">
#     <div class="floating-shape" style="width: 100px; height: 100px; top: 10%; left: 10%; animation-delay: 0s;"></div>
#     <div class="floating-shape" style="width: 150px; height: 150px; top: 70%; right: 10%; animation-delay: 2s;"></div>
#     <div class="floating-shape" style="width: 80px; height: 80px; top: 50%; left: 80%; animation-delay: 4s;"></div>
# </div>
# """, unsafe_allow_html=True)

# # Initialize session state
# if 'flashcards' not in st.session_state:
#     st.session_state.flashcards = None
# if 'generation_time' not in st.session_state:
#     st.session_state.generation_time = 0
# if 'current_subject' not in st.session_state:
#     st.session_state.current_subject = ""

# # --- Enhanced Sidebar ---
# with st.sidebar:
#     st.markdown("### 🎯 Quick Guide")
    
#     with st.expander("📚 How to Use", expanded=True):
#         st.markdown("""
#         **Step 1:** Choose your input method  
#         **Step 2:** Add your study material  
#         **Step 3:** Set subject & difficulty  
#         **Step 4:** Generate flashcards  
#         **Step 5:** Export and study!
#         """)
    
#     with st.expander("💡 Pro Tips"):
#         st.markdown("""
#         • Use clear, well-structured content
#         • Specify subject for better results
#         • Try different difficulty levels
#         • Export to your favorite study app
#         """)
    
#     with st.expander("📊 Supported Formats"):
#         st.markdown("""
#         **Input:** PDF, TXT, Plain Text  
#         **Export:** CSV, JSON, Anki, Print
#         """)
    
#     st.markdown("---")
    
#     # Stats section
#     if st.session_state.flashcards:
#         st.markdown("### 📈 Session Stats")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("Cards", len(st.session_state.flashcards))
#         with col2:
#             st.metric("Time", f"{st.session_state.generation_time:.1f}s")
    
#     st.markdown("---")
    
#     if st.button("🔄 New Session", type="secondary", use_container_width=True):
#         for key in list(st.session_state.keys()):
#             del st.session_state[key]
#         st.rerun()

# # --- Main Header ---
# st.markdown('<h1 class="main-header">🧠 AI Flashcard Generator Pro</h1>', unsafe_allow_html=True)
# st.markdown('<p class="subtitle">Transform any content into intelligent study flashcards with AI</p>', unsafe_allow_html=True)

# # --- Input Section with Enhanced Design ---
# st.markdown('<div class="input-container">', unsafe_allow_html=True)

# # Input method selection with icons
# col1, col2, col3 = st.columns([2, 1, 1])
# with col1:
#     input_method = st.radio(
#         "📝 Choose Input Method:",
#         ["✍️ Text Input", "📁 File Upload"],
#         horizontal=True,
#         key="input_method"
#     )

# with col2:
#     difficulty = st.selectbox(
#         "🎯 Difficulty:",
#         ["Easy", "Medium", "Hard"],
#         index=1,
#         key="difficulty"
#     )

# with col3:
#     num_cards = st.selectbox(
#         "🔢 Target Cards:",
#         [5, 10, 15],
#         index=2,
#         key="num_cards"
#     )

# # Subject input with emoji
# subject = st.text_input(
#     "📚 Subject (Optional):", 
#     placeholder="e.g., Biology, History, Computer Science...",
#     key="subject"
# )

# # Content input based on method
# if "Text Input" in input_method:
#     content = st.text_area(
#         "📝 Paste your study material here:",
#         height=300,
#         placeholder="Lecture notes, textbook content, research papers, or any study material...\n\nTip: The more structured your content, the better the flashcards!",
#         key="text_content"
#     )
# else:
#     content = st.file_uploader(
#         "📁 Upload your study file:",
#         type=["pdf", "txt"],
#         help="Supported formats: PDF or plain text files",
#         key="file_content"
#     )

# st.markdown('</div>', unsafe_allow_html=True)

# # --- Enhanced Generation Button ---
# generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])
# with generate_col2:
#     if st.button("✨ Generate Smart Flashcards", type="primary", use_container_width=True):
#         if content:
#             # Progress bar animation
#             progress_placeholder = st.empty()
#             status_placeholder = st.empty()
            
#             start_time = time.time()
            
#             # Animated progress bar
#             for i in range(101):
#                 progress_placeholder.markdown(f"""
#                 <div class="progress-container">
#                     <div class="progress-bar" style="width: {i}%"></div>
#                 </div>
#                 """, unsafe_allow_html=True)
                
#                 if i < 30:
#                     status_placeholder.info("🔍 Analyzing content...")
#                 elif i < 60:
#                     status_placeholder.info("🧠 Generating questions...")
#                 elif i < 90:
#                     status_placeholder.info("✅ Creating answers...")
#                 else:
#                     status_placeholder.info("🎉 Finalizing flashcards...")
                
#                 time.sleep(0.02)
            
#             try:
#                 generator = FlashcardGenerator()
                
#                 if "Text Input" in input_method:
#                     flashcards = generator.process_text(content, subject, difficulty)
#                 else:
#                     temp_path = os.path.join("/tmp", content.name)
#                     with open(temp_path, "wb") as f:
#                         content.seek(0)
#                         f.write(content.read())
#                     flashcards = generator.process_file(temp_path, subject, difficulty)
#                     os.remove(temp_path)
                
#                 end_time = time.time()
#                 st.session_state.generation_time = end_time - start_time
#                 st.session_state.flashcards = flashcards
#                 st.session_state.current_subject = subject or "General"
                
#                 progress_placeholder.empty()
#                 status_placeholder.success(f"🎉 Successfully generated {len(flashcards)} flashcards in {st.session_state.generation_time:.1f} seconds!")
                
#                 # Celebration animation
#                 st.balloons()
                
#             except Exception as e:
#                 progress_placeholder.empty()
#                 status_placeholder.error(f"❌ Error: {str(e)}")
#         else:
#             st.warning("⚠️ Please provide some content first!")

# # --- Display Statistics ---
# if st.session_state.flashcards:
#     st.markdown("---")
    
#     # Stats cards
#     st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    
#     stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
#     with stats_col1:
#         st.markdown(f"""
#         <div class="stat-card">
#             <div class="stat-number">{len(st.session_state.flashcards)}</div>
#             <div class="stat-label">Total Cards</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with stats_col2:
#         easy_count = sum(1 for card in st.session_state.flashcards if card.get('difficulty', '').lower() == 'easy')
#         st.markdown(f"""
#         <div class="stat-card">
#             <div class="stat-number">{easy_count}</div>
#             <div class="stat-label">Easy Cards</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with stats_col3:
#         medium_count = sum(1 for card in st.session_state.flashcards if card.get('difficulty', '').lower() == 'medium')
#         st.markdown(f"""
#         <div class="stat-card">
#             <div class="stat-number">{medium_count}</div>
#             <div class="stat-label">Medium Cards</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with stats_col4:
#         hard_count = sum(1 for card in st.session_state.flashcards if card.get('difficulty', '').lower() == 'hard')
#         st.markdown(f"""
#         <div class="stat-card">
#             <div class="stat-number">{hard_count}</div>
#             <div class="stat-label">Hard Cards</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown('</div>', unsafe_allow_html=True)

# # --- Enhanced Flashcard Display ---
# if st.session_state.flashcards:
#     st.markdown(f"## 🎴 Your {st.session_state.current_subject} Flashcards")
    
#     # Filter options
#     filter_col1, filter_col2, filter_col3 = st.columns(3)
#     with filter_col1:
#         show_difficulty = st.selectbox("Filter by Difficulty:", ["All", "Easy", "Medium", "Hard"])
#     with filter_col2:
#         cards_per_row = st.selectbox("Cards per Row:", [1, 2, 3], index=1)
#     with filter_col3:
#         sort_by = st.selectbox("Sort by:", ["Order", "Question Length"])
    
#     # Filter flashcards
#     filtered_cards = st.session_state.flashcards
#     if show_difficulty != "All":
#         filtered_cards = [card for card in filtered_cards if card.get('difficulty', '').lower() == show_difficulty.lower()]
    
#     # Sort flashcards
#     if sort_by == "Question Length":
#         filtered_cards = sorted(filtered_cards, key=lambda x: len(x['question']))
    
#     # Display flashcards
#     if filtered_cards:
#         cols = st.columns(cards_per_row)
#         for i, card in enumerate(filtered_cards):
#             with cols[i % cards_per_row]:
#                 card_difficulty = card.get('difficulty', difficulty).lower()
                
#                 st.markdown(f"""
#                 <div class="flashcard-modern">
#                     <div class="question-text">
#                         ❓ {card['question']}
#                     </div>
#                     <div class="answer-text">
#                         <strong>💡 Answer:</strong><br>
#                         {card['answer']}
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
#     else:
#         st.info("No flashcards match the selected filters.")

#     # --- Enhanced Export Section ---
#     st.markdown("---")
#     st.markdown("## 📤 Export Your Flashcards")
    
#     export_col1, export_col2, export_col3 = st.columns(3)
    
#     with export_col1:
#         csv_data = Exporter.to_csv_string(st.session_state.flashcards)
#         st.download_button(
#             "📊 Download CSV",
#             data=csv_data,
#             file_name=f"flashcards_{st.session_state.current_subject.lower().replace(' ', '_')}_{difficulty.lower()}.csv",
#             mime="text/csv",
#             use_container_width=True
#         )
    
#     with export_col2:
#         json_data = Exporter.to_json_string(st.session_state.flashcards)
#         st.download_button(
#             "📋 Download JSON",
#             data=json_data,
#             file_name=f"flashcards_{st.session_state.current_subject.lower().replace(' ', '_')}_{difficulty.lower()}.json",
#             mime="application/json",
#             use_container_width=True
#         )
    
#     with export_col3:
#         anki_data = Exporter.to_anki_string(st.session_state.flashcards)
#         st.download_button(
#             "🃏 Download for Anki",
#             data=anki_data,
#             file_name=f"flashcards_{st.session_state.current_subject.lower().replace(' ', '_')}_{difficulty.lower()}.txt",
#             mime="text/plain",
#             use_container_width=True
#         )
    
#     # Study tips
#     with st.expander("📚 Study Tips & Recommendations"):
#         st.markdown("""
#         ### 🎯 Effective Study Strategies:
        
#         **Spaced Repetition:** Review cards at increasing intervals (1 day, 3 days, 1 week, 2 weeks)
        
#         **Active Recall:** Try to answer before flipping the card
        
#         **Mix Difficulties:** Combine easy and hard cards in study sessions
        
#         **Regular Practice:** 15-20 minutes daily is better than long cramming sessions
        
#         **Track Progress:** Use apps like Anki or Quizlet to monitor your improvement
#         """)

# # --- Footer ---
# st.markdown("---")
# st.markdown("""
# <div style="text-align: center; padding: 2rem; color: #64748b;">
#     <h4>🚀 AI Flashcard Generator Pro</h4>
#     <p>Powered by Google Gemini • Built with ❤️ using Streamlit</p>
#     <p><small>© 2024 • Transform the way you study with AI</small></p>
# </div>
# """, unsafe_allow_html=True)



# frontend.py

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
    © 2025 <strong>AI Flashcard Generator</strong> | Crafted with ❤️ | Powered by <strong>Google Gemini</strong>
</div>
""", unsafe_allow_html=True)
