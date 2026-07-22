import os
import tempfile
from database import QuizDatabase
from generator import QuizGenerator
from renderer import SlideRenderer
from scheduler import SlideScheduler
from video_gen import VideoGenerator
from uploader import YouTubeUploader
from utils import cleanup_dir

class ShortCreator:
    def __init__(self, config):
        self.config = config
        self.db = QuizDatabase(config.DB_PATH)
        self.generator = QuizGenerator(config.OPENAI_API_KEY)
        self.renderer = SlideRenderer(config.FONT_PATH)
        self.scheduler = SlideScheduler(self.renderer)
        self.video_gen = VideoGenerator()
        self.uploader = YouTubeUploader(config.YOUTUBE_CREDENTIALS_PATH)

    def process_next(self):
        q = self.db.get_next_pending()
        if not q:
            print("No pending quiz found. Generating new ones...")
            new_quizzes = self.generator.generate_quizzes()
            for nq in new_quizzes:
                self.db.insert_quiz(nq)
            q = self.db.get_next_pending()
            if not q:
                print("No quiz generated. Retrying later.")
                return

        print(f"Processing quiz {q['id']}: {q['question']}")
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                slides = self.scheduler.schedule_all(q, q['id'], temp_dir)
                audio_path = os.path.join(temp_dir, "audio.mp3")
                self.video_gen.generate_audio_track(slides, audio_path)
                video_path = os.path.join(self.config.OUTPUT_DIR, f"short_{q['id']}.mp4")
                self.video_gen.create_video(slides, audio_path, video_path)
                
                video_id = self.uploader.upload_video(
                    video_path,
                    title=f"Trivia Quiz: {q['question'][:50]}...",
                    description=f"Test your knowledge! {q['question']}\n\n#shorts #quiz #trivia"
                )
                
                if video_id:
                    self.db.mark_completed(q['id'], video_id)
                    print(f"Successfully processed and uploaded quiz {q['id']} to YouTube: {video_id}")
                else:
                    print(f"Uploaded failed for quiz {q['id']}")
        except Exception as e:
            print(f"Error processing quiz {q['id']}: {e}")