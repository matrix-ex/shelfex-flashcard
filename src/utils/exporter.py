import csv
import json
import io

class Exporter:
    @staticmethod
    def to_csv_string(flashcards):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Question", "Answer", "Difficulty"])
        for card in flashcards:
            writer.writerow([card["question"], card["answer"], card["difficulty"]])
        return output.getvalue()

    @staticmethod
    def to_json_string(flashcards):
        return json.dumps(flashcards, indent=2, ensure_ascii=False)

    @staticmethod
    def to_anki_string(flashcards):
        return "\n".join([f"{card['question']}\t{card['answer']}" for card in flashcards])