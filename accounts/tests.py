from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountFlowTests(TestCase):
    def test_register_creates_user_and_logs_them_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("home"))
        self.assertTrue(User.objects.filter(username="newuser", email="newuser@example.com").exists())
        self.assertEqual(int(self.client.session["_auth_user_id"]), User.objects.get(username="newuser").pk)

    def test_logout_requires_post(self):
        user = User.objects.create_user(username="existing", password="StrongPass123!")
        self.client.force_login(user)

        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 405)

    def test_register_rejects_duplicate_email(self):
        User.objects.create_user(username="existing", email="taken@example.com", password="StrongPass123!")

        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "taken@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "An account with this email already exists.")
