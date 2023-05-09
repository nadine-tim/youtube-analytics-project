import os
from googleapiclient.discovery import build
from src.videoNotFound import VideoNotFound


class Video:
    """Класс для видео с ютуба"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        try:
            video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
            if len(video['items']) == 0:
                raise VideoNotFound
            self.title = video['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/channel/{video_id}"
            self.view_count = video['items'][0]['statistics']['viewCount']
            self.like_count = video['items'][0]['statistics']['likeCount']

        except VideoNotFound:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str) -> None:
        """Экземпляр инициализируется id видео и плейлиста."""

        super().__init__(video_id)
        self.playlist_id = playlist_id
