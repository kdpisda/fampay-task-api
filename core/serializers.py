from rest_framework import serializers
from core import models as core_models

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'title', 'description', 'published_at', 'thumbnails', 'youtube_video_id']
        model = core_models.Video