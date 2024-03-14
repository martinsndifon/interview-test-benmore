"""
views for the project APIs.
"""

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from core.models import Project
from project import serializers

from django.db.models import Q


@extend_schema(tags=["projects"])
class ProjectViewSet(viewsets.ModelViewSet):
    """Manage projects in the database."""

    serializer_class = serializers.ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """Retrieve the projects created by and projects that have tasks assigned to the authenticated user."""
        user = self.request.user

        return (
            Project.objects.filter(Q(user=user) | Q(task__assigned=user))
            .distinct()
            .order_by("-id")
        )

    def perform_create(self, serializer):
        """Create a new project."""
        serializer.save(user=self.request.user)
