import sqlite3
import json

class QuizDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS quizzes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT,
                    options TEXT,
                    answer TEXT,
                    explanation_chunks TEXT,
                    status TEXT DEFAULT 'pending',
                    video_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def insert_quiz(self, q):
        with self.conn:
            self.conn.execute("""
                INSERT INTO quizzes (question, options, answer, explanation_chunks)
                VALUES (?, ?, ?, ?)
            """, (
                q['question'],
                json.dumps(q['options']),
                q['answer'],
                json.dumps(q['explanationChunks'])
            ))

    def get_next_pending(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM quizzes WHERE status = 'pending' ORDER BY id LIMIT 1")
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'question': row[1],
                'options': json.loads(row[2]),
                'answer': row[3],
                'explanationChunks': json.loads(row[4]),
                'status': row[5]
            }
        return None

    def mark_completed(self, quiz_id, video_id):
        with self.conn:
            self.conn.execute("""
                UPDATE quizzes SET status = 'completed', video_id = ? WHERE id = ?
            """, (video_id, quiz_id))