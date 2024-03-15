"""
views for the Task APIs.
"""

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.authentication import TokenAuthentication

from core.models import Task
from task import serializers

from django.db.models import Q

from rest_framework.decorators import action
from rest_framework.response import Response


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


@extend_schema(tags=["task"])
class FilterTaskViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """View for managing filtering tasks by status"""

    serializer_class = serializers.TaskSerializer
    queryset = Task.objects.filter(completed=True).all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


@extend_schema(tags=["task"])
class CompleteTaskViewSet(viewsets.GenericViewSet):
    """View for marking tasks as complete"""

    serializer_class = serializers.TaskSerializer
    queryset = Task.objects.none()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"])
    def mark_task_as_complete(self, request, pk=None):
        """Mark the status of a task as complete"""
        try:
            task_id = int(pk)
        except ValueError:
            return Response(
                {"detail": "Invalid task ID."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.update(task, validated_data={"completed": True})
        return Response(serializer.data, status=status.HTTP_200_OK)
