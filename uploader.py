import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

class YouTubeUploader:
    def __init__(self, credentials_path=None):
        self.creds = None
        if credentials_path and os.path.exists(credentials_path):
            self.creds = Credentials.from_authorized_user_file(credentials_path, [
                "https://www.googleapis.com/auth/youtube.upload"
            ])

    def upload_video(self, video_path, title, description, category_id="27", privacy_status="private"):
        if not self.creds:
            print("Credentials not available. Skipping YouTube upload.")
            return None
        
        youtube = build("youtube", "v3", credentials=self.creds)
        body = {
            "snippet": {
                "title": title[:100],
                "description": description[:5000],
                "tags": ["quiz", "trivia", "education", "shorts"],
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": privacy_status
            }
        }
        
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")
        
        print("Upload complete!")
        return response.get("id")