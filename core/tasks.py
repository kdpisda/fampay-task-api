from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.files import File
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta

from core import models as core_models
from core import helpers as core_helpers

logger = get_task_logger(__name__)

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

@shared_task
def update_database():
    key_id = core_helpers.get_active_key()
    
    if key_id is None:
        logger.info("Key exhausted! Please enter a new key in the database")
        return
    
    key = core_models.Key.objects.get(pk=key_id)
    DEVELOPER_KEY = key.key
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    published_before_time = datetime.utcnow() 
    published_after_time = datetime.utcnow() - timedelta(hours=1)

    # 2020-10-15T01:24:41Z
    published_before_time_str = published_before_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    published_after_time_str = published_after_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    search_response = youtube.search().list(
        q=settings.SEARCH_KEYWORD,
        part='id,snippet',
        maxResults=1000,
        publishedAfter=published_after_time_str,
        publishedBefore=published_before_time_str
    ).execute()

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video, _ = core_models.Video.objects.get_or_create(youtube_video_id=search_result['id']['videoId'])
            video.title = search_result['snippet']['title']
            video.description = search_result['snippet']['description']
            video.published_at = search_result['snippet']['publishedAt']
            video.thumbnails = search_result['snippet']['thumbnails']
            video.raw = search_result
            video.save()
