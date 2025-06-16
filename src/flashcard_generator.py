#flashcard_generator  
from utils.gemini_integration import GeminiIntegration
from utils.file_processor import FileProcessor

class FlashcardGenerator:
    def __init__(self):
        self.gemini = GeminiIntegration()
        self.file_processor = FileProcessor()

    def process_text(self, text, subject=None, difficulty_level="Medium"):
        raw_flashcards = self.gemini.generate_flashcards(text, subject, difficulty_level)
        if not raw_flashcards:
            return None
        return self._parse_flashcards(raw_flashcards, difficulty_level)

    def process_file(self, file_path, subject=None, difficulty_level="Medium"):
        if file_path.endswith('.txt'):
            text = self.file_processor.read_txt(file_path)
        elif file_path.endswith('.pdf'):
            text = self.file_processor.read_pdf(file_path)
        else:
            raise ValueError("Unsupported file format")
        return self.process_text(text, subject, difficulty_level)

    def _parse_flashcards(self, raw_text, difficulty_level):
        flashcards = []
        current_card = {"question": None, "answer": None, "difficulty": difficulty_level}
        
        for line in raw_text.split('\n'):
            line = line.strip()
            if line.startswith('Q:'):
                if current_card["question"]:
                    flashcards.append(current_card.copy())
                current_card = {
                    "question": line[2:].strip(),
                    "answer": None,
                    "difficulty": difficulty_level
                }
            elif line.startswith('A:'):
                current_card["answer"] = line[2:].strip()
            elif line.startswith('D:'):
                current_card["difficulty"] = line[2:].strip()
            elif line == '---' and current_card["question"]:
                flashcards.append(current_card.copy())
                current_card = {"question": None, "answer": None, "difficulty": difficulty_level}
        
        if current_card["question"]:
            flashcards.append(current_card)
        
        # Filter by selected difficulty
        return [card for card in flashcards if card["difficulty"].lower() == difficulty_level.lower()]