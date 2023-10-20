from rest_framework import serializers
from .models import Like

class LikeCreateSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='author.username')

    def create(self, validated_data):
        author = validated_data.pop('author', None)

        if not author:
            raise serializers.ValidationError("Author is required.")

        like = Like.objects.create(author=author, **validated_data)
        return like

    class Meta:
        fields = (
            "like_id",
            "username",
            "post",
        )
        model = Like
