"""
views for the Task APIs.
"""

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.authentication import TokenAuthentication

from core.models import Task
from task import serializers

from django.db.models import Q


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user


@extend_schema(tags=["task"])
class TaskViewSet(viewsets.ModelViewSet):
    """Manage tasks in the database."""

    serializer_class = serializers.TaskSerializer
    queryset = Task.objects.all()
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """Retrieve the tasks created by and assigned to the authenticated user."""
        user = self.request.user

        return (
            Task.objects.filter(Q(user=user) | Q(assigned=user))
            .distinct()
            .order_by("-id")
        )

    def get_permissions(self):
        """Return permissions based on the request action."""
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsOwnerPermission]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Create a new Task."""
        serializer.save(user=self.request.user)
