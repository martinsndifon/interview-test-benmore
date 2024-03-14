"""
views for the project APIs.
"""

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.authentication import TokenAuthentication

from core.models import Project
from project import serializers

from django.db.models import Q


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user


@extend_schema(tags=["projects"])
class ProjectViewSet(viewsets.ModelViewSet):
    """Manage projects in the database."""

    serializer_class = serializers.ProjectSerializer
    queryset = Project.objects.all()
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """Retrieve the projects created by and projects that have tasks assigned to the authenticated user."""
        user = self.request.user

        return (
            Project.objects.filter(Q(user=user) | Q(task__assigned=user))
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
        """Create a new project."""
        serializer.save(user=self.request.user)
