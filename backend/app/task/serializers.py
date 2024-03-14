"""
Serializer for Task APIs.
"""

from rest_framework import serializers
from user.serializers import UserSerializer

from core.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task objects."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "due_date",
            "completed",
            "assigned",
            "project",
            "user",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
