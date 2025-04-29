from django.db import models
from django.conf import settings

class Diary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="diaries")
    date = models.DateField()
    lunar_date = models.CharField(max_length=10)
    content = models.TextField()
    weather = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.nickname} - {self.date} 농사일지"