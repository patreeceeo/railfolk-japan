import hashlib

from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    short_bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_username()

    def get_gravatar_url(self, size):
        if type(size) is not int or size < 1:
            raise ValueError("size must be a positive integer")

        normalized_email = self.user.email.strip().lower()
        email_hash = hashlib.sha256(normalized_email.encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"
