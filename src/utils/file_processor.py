#pdf_input
from PyPDF2 import PdfReader

class FileProcessor:
    @staticmethod
    def read_txt(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def read_pdf(file_path):
        text = ""
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text()
        return text