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


class Location(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TransitLeg(models.Model):
    class Mode(models.TextChoices):
        TRAIN = "train", "Train"
        SHINKANSEN = "shinkansen", "Shinkansen"
        LIMITED_EXPRESS = "limited-express", "Limited express"
        BUS = "bus", "Bus"

    mode = models.CharField(max_length=20, choices=Mode.choices)
    origin = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="departing_transit_legs",
    )
    destination = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="arriving_transit_legs",
    )
    operator = models.CharField(max_length=100, blank=True)
    line_name = models.CharField(max_length=100, blank=True)
    fare_yen = models.PositiveIntegerField()
    duration_days = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.origin} to {self.destination}"


class VisitCard(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="visit_cards",
    )
    suggested_hours = models.DecimalField(max_digits=5, decimal_places=2)
    admission_yen = models.PositiveIntegerField()

    def __str__(self):
        return self.location.name


class EducationCard(models.Model):
    class Category(models.TextChoices):
        RAIL = "rail", "Rail"
        CULTURE = "culture", "Culture"
        LANGUAGE = "language", "Language"
        REGIONAL_CONTEXT = "regional-context", "Regional context"

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=Category.choices)
    body = models.TextField()
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="education_cards",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title
