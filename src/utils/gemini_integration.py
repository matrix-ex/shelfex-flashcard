#api_intigration
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

class GeminiIntegration:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("API key not found in .env")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')

    def generate_flashcards(self, content, subject=None, difficulty_level="Medium"):
        prompt = f"""
        Create {difficulty_level}-level flashcards from this content:
        {content}
        {"Subject: " + subject if subject else ""}

        Follow these rules STRICTLY:
        1. Generate 10-15 flashcards
        2. Each flashcard must have:
           Q: [clear question]
           A: [concise answer]
           D: [{difficulty_level}]
        3. Questions should test {difficulty_level.lower()} knowledge:
           - Easy: Basic facts and definitions
           - Medium: Application of concepts
           - Hard: Analysis, synthesis, or complex scenarios
        4. Format exactly like this example:
           Q: What is photosynthesis?
           A: The process plants use to convert sunlight into energy
           D: Easy
           ---

        Now generate the flashcards:
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7 if difficulty_level == "Hard" else 0.3,
                    max_output_tokens=2000
                )
            )
            if not response.text:
                raise ValueError("Empty response from API")
            return response.text
        except Exception as e:
            print(f"API Error: {str(e)}")
            return None