# 🧠 AI Flashcard Generator    
*Automatically convert study materials into interactive flashcards using Google Gemini AI*

## ✨ Features  
- **Multi-Input Support**: Process text directly or upload PDF/TXT files  
- **Smart Difficulty Levels**: Generate Easy/Medium/Hard questions  
- **Export Options**: Download flashcards as CSV or JSON  
- **PDF Processing**: Extract text from textbooks and lecture notes  
- **Responsive Web UI**: Built with Streamlit for seamless interaction  

## 🛠️ Installation  

### Requirements  
- Python 3.8+  
- Google Gemini API key ([Get API key](https://aistudio.google.com/))  

## Setup  

#### 1. Clone repository
```bash
git clone https://github.com/yourusername/flashcard-generator.git
cd flashcard-generator
```
#### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure API key
```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

## 🚀 Usage
 
#### 1. Start the application:
```bash
streamlit run main.py
```

#### 2. Input your content:
- Paste text directly
- Upload PDF or TXT files (≤10MB)

#### 3. Configure settings:
- Set subject (optional)
- Select difficulty level

#### 4. Generate & Export:
- Review AI-generated flashcards
- Download in CSV or JSON format

## 🏗️ Architecture
```bash
project/
├── utils/
│   ├── exporter.py           # CSV/JSON export handlers
│   ├── file_processor.py     # PDF/TXT text extraction
│   └── gemini_integration.py # Gemini API communication
├── flashcard_generator.py    # Core processing logic
├── main.py                   # Streamlit application
├── .gitignore
├── README.md
└── requirements.txt
```

