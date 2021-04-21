from django.contrib import admin
from core import models as core_models

# Register your models here.
class KeyAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'created_at']

class KeyUsageAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'date', 'expired', 'created_at']
    list_filter = ('expired',)

class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'youtube_video_id', 'title', 'created_at']

admin.site.register(core_models.Key, KeyAdmin)
admin.site.register(core_models.KeyUsage, KeyUsageAdmin)
admin.site.register(core_models.Video, VideoAdmin)