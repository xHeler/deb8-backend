import uuid
from django.db import models
from accounts.models import User
from posts.models import Post


class Like(models.Model):
    like_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"User: {self.author.username} likes: Post: {self.post}"
    
    class Meta:
        unique_together = ('post', 'author')