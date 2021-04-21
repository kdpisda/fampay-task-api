from django.db import models

# Create your models here.
class Key(models.Model):
    key = models.CharField(max_length=64, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Keys"
    
    def __str__(self):
        return "{} [{}]".format(self.pk, self.key)

class KeyUsage(models.Model):
    key = models.ForeignKey(Key, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Key Usages"

    def __str__(self):
        return "{} [{}][{}]".format(self.key, self.date, self.expired)

class Video(models.Model):
    title = models.TextField()
    description = models.TextField()
    published_at = models.DateTimeField(null=True, blank=True)
    thumbnails = models.JSONField(null=True, blank=True)
    raw = models.JSONField(null=True, blank=True)
    youtube_video_id = models.CharField(max_length=16, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Videos"