import os

class Config:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.YOUTUBE_CREDENTIALS_PATH = os.getenv("YOUTUBE_CREDENTIALS_PATH", "youtube_creds.json")
        self.OUTPUT_DIR = "output"
        self.TEMP_DIR = "temp"
        self.POLL_INTERVAL = 60
        self.FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        self.DB_PATH = "quiz.db"