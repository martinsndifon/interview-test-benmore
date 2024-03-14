"""
Serializer for Project APIs.
"""

from rest_framework import serializers
from user.serializers import UserSerializer

from core.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project objects."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "task",
            "description",
            "created_at",
            "updated_at",
            "due_date",
            "user",
        ]
        read_only_fields = ["id", "task", "created_at", "updated_at"]
