from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from core import models as core_models
from django.core.files import File
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta

logger = get_task_logger(__name__)

@shared_task
def update_database():
    pass