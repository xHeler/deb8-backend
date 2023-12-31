import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from posts.models import Post
from accounts.models import User

class Comment(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=150, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])

    def __str__(self):
        text = self.text[:20] + "..."
        return f"User: {self.author.username} - Post: {self.post.post_id} |  {text}"