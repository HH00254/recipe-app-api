"""
Serializers for the comments API.
"""

from comments.models import Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""

    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_name = serializers.CharField(source="user.name", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "user_email", "user_name", "created_at", "updated_at"]
        read_only_fields = ["id", "user_email", "user_name", "created_at", "updated_at"]
