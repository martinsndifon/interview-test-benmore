"""
Database Models.
"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User database model."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Project(models.Model):
    """Project object."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    task = models.ManyToManyField("Task", related_name="tasks", blank=True)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation of the project."""
        return self.title


class Task(models.Model):
    """Task object."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    assigned = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="assigned_users", blank=True
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="task_project"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation of the task."""
        return self.title

    def save(self, *args, **kwargs):
        """Override save method to update project tasks."""
        super().save(*args, **kwargs)
        if self.project:
            self.project.task.add(self)

    def delete(self, *args, **kwargs):
        """Override delete method to remove task from project tasks."""
        if self.project:
            self.project.task.remove(self)
        super().delete(*args, **kwargs)
