from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'author', 'post', 'text', 'created_at')
    

admin.site.register(Comment, CommentAdmin)