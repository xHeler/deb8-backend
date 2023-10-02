import uuid
from django.db import models
from accounts.models import User


class Post(models.Model):
    post_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    image_url = models.URLField(max_length=500)
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or str(self.post_id)
