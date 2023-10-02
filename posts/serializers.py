from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
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
