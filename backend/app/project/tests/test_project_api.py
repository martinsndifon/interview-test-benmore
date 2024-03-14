"""
Test for project APIs
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Project

from project.serializers import ProjectSerializer

PROJECT_URL = reverse("project:project-list")


def detail_url(project_id):
    """Return project detail URL."""
    return reverse("project:project-detail", args=[project_id])


def create_sample_project(user, **params):
    """Create and return a sample project."""
    defaults = {
        "title": "Sample Project",
        "description": "Sample Description",
        "due_date": "2024-03-14T10:20:30Z",
    }
    defaults.update(params)

    return Project.objects.create(user=user, **defaults)


class PublicProjectApiTests(TestCase):
    """Test the publicly available project API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@example.com", "testpass123"
        )

    def test_login_required(self):
        """Test that login is required for retrieving projects."""
        res = self.client.get(PROJECT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_for_detail(self):
        """Test that login is required for retrieving project detail."""
        project = create_sample_project(user=self.user)
        url = detail_url(project.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_for_create(self):
        """Test that login is required for creating project."""
        res = self.client.post(PROJECT_URL, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_for_update(self):
        """Test that login is required for updating project."""
        project = create_sample_project(user=self.user)
        url = detail_url(project.id)
        res = self.client.put(url, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_for_partial_update(self):
        """Test that login is required for partially updating project."""
        project = create_sample_project(user=self.user)
        url = detail_url(project.id)
        res = self.client.patch(url, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_for_delete(self):
        """Test that login is required for deleting project."""
        project = create_sample_project(user=self.user)
        url = detail_url(project.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProjectApiTests(TestCase):
    """Test the authorized user project API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@example.com", "testpass123"
        )
        self.client.force_authenticate(self.user)

    def test_create_project_successful(self):
        """Test creating a new project."""
        payload = {
            "title": "Sample Project",
            "description": "Sample Description",
            "due_date": "2024-03-14T10:20:30Z",
        }
        res = self.client.post(PROJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        project = Project.objects.get(id=res.data["id"])
        for key in payload.keys():
            if key == "due_date":
                pass
            else:
                self.assertEqual(payload[key], getattr(project, key))

    def test_create_project_invalid(self):
        """Test creating a new project with invalid payload."""
        payload = {
            "title": "",
            "description": "",
            "due_date": "",
        }
        res = self.client.post(PROJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_projects(self):
        """Test retrieving projects."""
        create_sample_project(user=self.user)
        create_sample_project(user=self.user)

        res = self.client.get(PROJECT_URL)

        projects = Project.objects.all().order_by("-id")
        serializer = ProjectSerializer(projects, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_project_detail(self):
        """Test retrieving project detail."""
        project = create_sample_project(user=self.user)

        url = detail_url(project.id)
        res = self.client.get(url)

        serializer = ProjectSerializer(project)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_project(self):
        """Test updating a project."""
        project = create_sample_project(user=self.user)
        payload = {
            "title": "Updated Title",
            "description": "Updated Description",
            "due_date": "2024-03-14T10:20:30Z",
        }
        url = detail_url(project.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        project.refresh_from_db()
        for key in payload.keys():
            if key == "due_date":
                pass
            else:
                self.assertEqual(payload[key], getattr(project, key))

    def test_partial_update_project(self):
        """Test partially updating a project."""
        project = create_sample_project(user=self.user)
        payload = {"title": "Updated Title"}
        url = detail_url(project.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        project.refresh_from_db()
        self.assertEqual(payload["title"], project.title)

    def test_delete_project(self):
        """Test deleting a project."""
        project = create_sample_project(user=self.user)
        url = detail_url(project.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.filter(id=project.id).count(), 0)

    def test_deleting_project_not_owned(self):
        """Test deleting a project not owned by the user."""
        user2 = get_user_model().objects.create_user("user2@exampl.com", "testpass123")
        project = create_sample_project(user=user2)
        url = detail_url(project.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Project.objects.filter(id=project.id).count(), 1)

    def test_updating_project_not_owned(self):
        """Test updating a project not owned by the user."""
        user2 = get_user_model().objects.create_user("user2@example.com", "testpass123")
        project = create_sample_project(user=user2)
        payload = {"title": "Updated Title"}
        url = detail_url(project.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        project.refresh_from_db()
        self.assertNotEqual(payload["title"], project.title)
        self.assertEqual(project.title, "Sample Project")

    def test_partial_updating_project_not_owned(self):
        """Test partially updating a project not owned by the user."""
        user2 = get_user_model().objects.create_user("user2@example.com", "testpass123")
        project = create_sample_project(user=user2)
        payload = {"title": "Updated Title"}
        url = detail_url(project.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        project.refresh_from_db()
        self.assertNotEqual(payload["title"], project.title)
        self.assertEqual(project.title, "Sample Project")
