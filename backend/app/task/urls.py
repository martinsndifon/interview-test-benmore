"""URL mappings for the task app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from task import views

router = DefaultRouter()
router.register("", views.TaskViewSet)
router.register("status/filter", views.FilterTaskViewSet, basename="filter")
router.register("status/complete", views.CompleteTaskViewSet, basename="complete")

app_name = "task"

urlpatterns = [
    path("", include(router.urls)),
]
