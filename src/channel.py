import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

        self.channel_id = channel_id
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{channel_id}"
        self.subscribers_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.total_views = channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(f"Название: {self.title}")
        print(f"URL: {self.url}")
        print(f"Описание: {self.description}")
        print(f"Подписчиков: {self.subscribers_count}")
        print(f"Количество видео: {self.video_count}")
        print(f"Количество просмотров: {self.total_views}")

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, file_name: str) -> None:
        """Сохраняет значения атрибутов экземпляра в json-файл."""
        data = {
            'id': self.channel_id,
            'name': self.title,
            'description': self.description,
            'url': self.url,
            'subscribers_count': self.subscribers_count,
            'video_count': self.video_count,
            'total_views': self.total_views
        }
        with open(file_name, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
