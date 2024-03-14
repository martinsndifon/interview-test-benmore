"""
Test for Task APIs
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Task, Project

from task.serializers import TaskSerializer

TASK_URL = reverse("task:task-list")


def detail_url(task_id):
    """Return task detail URL."""
    return reverse("task:task-detail", args=[task_id])


def create_sample_task(user, **params):
    """Create and return a sample task."""
    defaults = {
        "title": "Sample task",
        "description": "Sample Description",
        "due_date": "2024-03-14T10:20:30Z",
    }
    defaults.update(params)

    return Task.objects.create(user=user, **defaults)


def create_sample_project(user, **params):
    """Create and return a sample project."""
    defaults = {
        "title": "Sample Project",
        "description": "Sample Description",
        "due_date": "2024-03-14T10:20:30Z",
    }
    defaults.update(params)

    return Project.objects.create(user=user, **defaults)


class PublicTasktApiTests(TestCase):
    """Test the publicly available Task API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@example.com", "testpass123"
        )

    def test_login_required(self):
        """Test that login is required for retrieving tasks."""
        res = self.client.get(TASK_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_for_detail(self):
        """Test that login is required for retrieving task detail."""
        project = create_sample_project(user=self.user)

        task = create_sample_task(user=self.user, project=project)
        url = detail_url(task.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_for_create(self):
        """Test that login is required for creating task."""
        res = self.client.post(TASK_URL, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_for_update(self):
        """Test that login is required for updating task."""
        project = create_sample_project(user=self.user)

        task = create_sample_task(user=self.user, project=project)
        url = detail_url(task.id)
        res = self.client.put(url, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_for_partial_update(self):
        """Test that login is required for partially updating task."""
        project = create_sample_project(user=self.user)

        task = create_sample_task(user=self.user, project=project)
        url = detail_url(task.id)
        res = self.client.patch(url, {})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_for_delete(self):
        """Test that login is required for deleting task."""
        project = create_sample_project(user=self.user)

        task = create_sample_task(user=self.user, project=project)
        url = detail_url(task.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTaskApiTests(TestCase):
    """Test the authorized user task API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@example.com", "testpass123"
        )
        self.client.force_authenticate(self.user)

    def test_create_task_successful(self):
        """Test creating a new task."""
        project = create_sample_project(user=self.user)
        payload = {
            "title": "Sample Project",
            "description": "Sample Description",
            "due_date": "2024-03-14T10:20:30Z",
            "project": project.id,
        }
        res = self.client.post(TASK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get(id=res.data["id"])
        for key in payload.keys():
            if key == "due_date":
                pass
            elif key == "project":
                self.assertEqual(payload[key], getattr(task, key).id)
            else:
                self.assertEqual(payload[key], getattr(task, key))

    def test_create_task_invalid(self):
        """Test creating a new task with invalid payload."""
        payload = {
            "title": "",
            "description": "",
            "due_date": "",
            "project": "",
        }
        res = self.client.post(TASK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tasks(self):
        """Test retrieving tasks."""
        project = create_sample_project(user=self.user)

        create_sample_task(user=self.user, project=project)
        create_sample_task(user=self.user, project=project)

        res = self.client.get(TASK_URL)

        tasks = Task.objects.all().order_by("-id")
        serializer = TaskSerializer(tasks, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_task_detail(self):
        """Test retrieving task detail."""
        project = create_sample_project(user=self.user)

        task = create_sample_task(user=self.user, project=project)

        url = detail_url(task.id)
        res = self.client.get(url)

        serializer = TaskSerializer(task)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_task(self):
        """Test updating a task."""
        project = create_sample_project(user=self.user)

        task = create_sample_task(user=self.user, project=project)
        payload = {
            "title": "Updated Title",
            "description": "Updated Description",
            "due_date": "2024-03-14T10:20:30Z",
            "project": project.id,
        }
        url = detail_url(task.id)
        self.client.put(url, payload)

        task.refresh_from_db()
        for key in payload.keys():
            if key == "due_date":
                pass
            elif key == "project":
                self.assertEqual(payload[key], getattr(task, key).id)
            else:
                self.assertEqual(payload[key], getattr(task, key))

    def test_partial_update_task(self):
        """Test partially updating a task."""
        project = create_sample_project(user=self.user)

        task = create_sample_task(user=self.user, project=project)
        payload = {"title": "Updated Title"}
        url = detail_url(task.id)
        self.client.patch(url, payload)

        task.refresh_from_db()
        self.assertEqual(payload["title"], task.title)

    def test_delete_task(self):
        """Test deleting a task."""
        project = create_sample_project(user=self.user)

        task = create_sample_task(user=self.user, project=project)
        url = detail_url(task.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.filter(id=task.id).count(), 0)

    def test_deleting_task_not_owned(self):
        """Test deleting a task not owned by the user."""
        user2 = get_user_model().objects.create_user("user2@exampl.com", "testpass123")

        project = create_sample_project(user=user2)

        task = create_sample_task(user=user2, project=project)
        url = detail_url(task.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Task.objects.filter(id=task.id).count(), 1)

    def test_updating_task_not_owned(self):
        """Test updating a task not owned by the user."""
        user2 = get_user_model().objects.create_user("user2@example.com", "testpass123")

        project = create_sample_project(user=user2)

        task = create_sample_task(user=user2, project=project)
        payload = {
            "title": "Updated Title",
            "description": "Updated Description",
            "due_date": "2024-03-14T10:20:30Z",
            "project": project.id,
        }
        url = detail_url(task.id)

        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        task.refresh_from_db()
        self.assertNotEqual(payload["title"], task.title)
        self.assertEqual(task.title, "Sample task")

    def test_partial_updating_task_not_owned(self):
        """Test partially updating a task not owned by the user."""
        user2 = get_user_model().objects.create_user("user2@example.com", "testpass123")

        project = create_sample_project(user=user2)

        task = create_sample_task(user=user2, project=project)
        payload = {"title": "Updated Title"}
        url = detail_url(task.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        task.refresh_from_db()
        self.assertNotEqual(payload["title"], task.title)
        self.assertEqual(task.title, "Sample task")
