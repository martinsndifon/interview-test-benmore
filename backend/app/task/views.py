"""
views for the Task APIs.
"""

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from core.models import Task
from task import serializers

from django.db.models import Q


@extend_schema(tags=["task"])
class TaskViewSet(viewsets.ModelViewSet):
    """Manage tasks in the database."""

    serializer_class = serializers.TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """Retrieve the tasks created by and assigned to the authenticated user."""
        user = self.request.user

        return (
            Task.objects.filter(Q(user=user) | Q(assigned=user))
            .distinct()
            .order_by("-id")
        )

    def perform_create(self, serializer):
        """Create a new Task."""
        serializer.save(user=self.request.user)
