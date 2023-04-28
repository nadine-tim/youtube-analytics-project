import datetime
import os
import isodate
from googleapiclient.discovery import build


class PlayList:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        playlist = self.youtube.playlists().list(part='snippet', id=playlist_id).execute()

        self.playlist_id = playlist_id
        self.title = playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"

    def __str__(self):
        return f"{self.title} ({self.url})"

    @property
    def total_duration(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        total_duration: datetime.timedelta = datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
                                                                minutes=0, hours=0, weeks=0)
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        most_likes = 0
        most_popular_video_id = ''
        for video_id in video_ids:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=video_id
                                                        ).execute()
            like_count = int(video_response['items'][0]['statistics']['likeCount'])
            if like_count > most_likes:
                most_popular_video_id = video_id

        return f'https://youtu.be/{most_popular_video_id}'
