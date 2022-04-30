from typing import Any
from googleapiclient.discovery import build

from .env import YOUTUBE_API_KEY


class YouTube:
    """
    Class for interacting with YouTube Data API v3
    """

    def __init__(self) -> Any:
        """
        Create a resource for interacting with YouTube Data API v3

        Returns:
            Any: The created resource
        """

        self._yt = build(
            serviceName="youtube",
            version="v3",
            developerKey=YOUTUBE_API_KEY
        )

    def search(self, query: str) -> Any:
        """
        Search for a youtube video

        Args:
            query (str): Search query
            channel (str, optional): Channel name. Defaults to "".

        Returns:
            Any: The URL(s) of search results
        """

        # Request body
        response = self._yt.search().list(
            part="id,snippet",
            type='video',
            q=query,
            maxResults=30
        ).execute()

        return [video for video in response["items"]]
