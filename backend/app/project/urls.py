"""URL mappings for the project app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from project import views

router = DefaultRouter()
router.register("", views.ProjectViewSet)
router.register(
    "projects/search", views.ProjectSearchViewSet, basename="project-search"
)

app_name = "project"

urlpatterns = [
    path("", include(router.urls)),
]
