from rest_framework import serializers

from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('comment_id', 'author', 'text', "rating")


class CommentCreateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    def create(self, validated_data):
        author = validated_data.pop('author', None)

        if not author:
            raise serializers.ValidationError("Author is required.")

        comment = Comment.objects.create(author=author, **validated_data)
        return comment

    class Meta:
        fields = ('author', 'post', 'text')
        model = Comment

class CommentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('comment_id',)
        model = Comment