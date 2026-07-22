import openai
import json

class QuizGenerator:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def generate_quizzes(self):
        prompt = """
        Generate 5 interesting trivia questions in JSON format. Each question should have:
        - question: The trivia question.
        - options: 4 multiple choice options.
        - answer: The correct option.
        - explanationChunks: A list of 2-3 short, engaging explanation points explaining the answer (each under 80 characters).
        
        Output must be a raw JSON array matching this structure.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)
            return data.get("quizzes", data) if isinstance(data, dict) else data
        except Exception as e:
            print(f"Error generating quizzes: {e}")
            return []