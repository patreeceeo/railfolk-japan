from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .models import UserProfile


class HomePageTests(SimpleTestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Railfolk Japan")


class UserProfileTests(TestCase):
    def test_get_gravatar_url_uses_normalized_email_sha256(self):
        user = get_user_model().objects.create_user(
            username="patreece",
            email=" Patreece@Example.COM ",
        )
        profile = UserProfile.objects.create(user=user)

        self.assertEqual(
            profile.get_gravatar_url(96),
            "https://www.gravatar.com/avatar/"
            "5fa578249e1f20c35509ca2dd16456e9f4a73f18b2cbf602e6a20e2b1d8ee3e2"
            "?s=96&d=identicon",
        )

    def test_get_gravatar_url_rejects_non_positive_size(self):
        user = get_user_model().objects.create_user(
            username="patreece",
            email="patreece@example.com",
        )
        profile = UserProfile.objects.create(user=user)

        with self.assertRaisesMessage(ValueError, "size must be a positive integer"):
            profile.get_gravatar_url(0)
