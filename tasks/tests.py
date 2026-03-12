from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskAuthorizationTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="StrongPass123!")
        self.other_user = User.objects.create_user(username="other", password="StrongPass123!")
        self.task = Task.objects.create(
            user=self.owner,
            title="Owner task",
            description="Keep private",
            priority="high",
        )

    def test_home_only_shows_authenticated_users_tasks(self):
        Task.objects.create(user=self.other_user, title="Other task", priority="low")
        self.client.force_login(self.owner)

        response = self.client.get(reverse("home"))

        self.assertContains(response, "Owner task")
        self.assertNotContains(response, "Other task")

    def test_user_cannot_edit_another_users_task(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse("edit_task", args=[self.task.pk]),
            {
                "title": "Hijacked",
                "description": "Attempted takeover",
                "priority": "low",
                "due_date": "",
            },
        )

        self.assertEqual(response.status_code, 404)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Owner task")

    def test_delete_requires_post(self):
        self.client.force_login(self.owner)

        response = self.client.get(reverse("delete_task", args=[self.task.pk]))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_user_cannot_delete_another_users_task(self):
        self.client.force_login(self.other_user)

        response = self.client.post(reverse("delete_task", args=[self.task.pk]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_create_task_assigns_current_user(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("create_task_submit"),
            {
                "title": "Fresh task",
                "description": "Created from test",
                "priority": "medium",
                "due_date": (date.today() + timedelta(days=2)).isoformat(),
            },
        )

        self.assertRedirects(response, reverse("home"))
        self.assertTrue(Task.objects.filter(user=self.owner, title="Fresh task").exists())

    def test_toggle_requires_owner(self):
        self.client.force_login(self.other_user)

        response = self.client.post(reverse("toggle_complete", args=[self.task.pk]))

        self.assertEqual(response.status_code, 404)
        self.task.refresh_from_db()
        self.assertFalse(self.task.completed)
