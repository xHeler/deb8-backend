from rest_framework import serializers

from likes.models import Like
from comments.models import Comment
from comments.serializers import CommentSerializer
from .models import Post


class PostCreateSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='author.username')

    def create(self, validated_data):
        author = validated_data.pop('author', None)

        if not author:
            raise serializers.ValidationError("Author is required.")

        post = Post.objects.create(author=author, **validated_data)
        return post

    class Meta:
        fields = (
            "post_id",
            "username",
            "title",
            "image",
            "description",
            "created_at",
        )
        model = Post


class PostReadSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return Like.objects.filter(post=obj).count()
    
    def get_comments_count(self, obj):
        return Comment.objects.filter(post=obj).count()

    def get_isLiked(self, obj):
        user = self.context['request'].user
        is_liked = Like.objects.filter(author=user, post=obj).exists()
        return is_liked

    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj)
        return CommentSerializer(comments, many=True).data

    class Meta:
        fields = (
            "post_id",
            "username",
            "title",
            "image",
            "description",
            "created_at",
            "likes_count",
            "comments_count",
            "comments",
            "isLiked",
        )
        model = Post