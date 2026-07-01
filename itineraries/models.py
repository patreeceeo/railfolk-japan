import secrets
from collections import OrderedDict
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.functions import Lower


def generate_avatar_key():
    return secrets.token_hex(16)


username_validator = RegexValidator(
    regex=r"^[A-Za-z0-9_-]{3,20}$",
    message="Username must be 3-20 characters and contain only letters, numbers, underscores, or hyphens.",
)


class User(AbstractUser):
    username = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        validators=[username_validator],
    )
    avatar_key = models.CharField(
        max_length=32,
        default=generate_avatar_key,
        editable=False,
        unique=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("username"),
                name="itineraries_user_username_ci_unique",
            ),
        ]


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    short_bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_username()


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
    duration_hours = models.PositiveIntegerField()

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


class Itinerary(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = "public", "Public"
        UNLISTED = "unlisted", "Unlisted"

    title = models.CharField(max_length=200)
    description = models.TextField()
    visibility = models.CharField(max_length=20, choices=Visibility.choices)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="itineraries",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    education_cards = models.ManyToManyField(
        EducationCard,
        related_name="itineraries",
        blank=True,
    )

    def __str__(self):
        return self.title

    def total_duration(self):
        earliest_start = None
        latest_end = None

        for attached_leg in self.attached_transit_legs.select_related("transit_leg"):
            if attached_leg.transit_leg.duration_hours < 1:
                raise ValueError("transit leg duration_hours must be positive")

            end_date = attached_leg.start_date + timedelta(
                days=(attached_leg.transit_leg.duration_hours - 1) // 24
            )
            earliest_start = min(
                earliest_start or attached_leg.start_date,
                attached_leg.start_date,
            )
            latest_end = max(latest_end or end_date, end_date)

        for attached_visit in self.attached_visit_cards.all():
            earliest_start = min(
                earliest_start or attached_visit.start_date,
                attached_visit.start_date,
            )
            latest_end = max(
                latest_end or attached_visit.start_date,
                attached_visit.start_date,
            )

        if earliest_start is None:
            return None

        return earliest_start, latest_end

    def grouped_by_date(self):
        grouped = OrderedDict()

        for attached_leg in self.attached_transit_legs.order_by("start_date", "id"):
            grouped.setdefault(
                attached_leg.start_date,
                {"transit_legs": [], "visit_cards": []},
            )["transit_legs"].append(attached_leg)

        for attached_visit in self.attached_visit_cards.order_by("start_date", "id"):
            grouped.setdefault(
                attached_visit.start_date,
                {"transit_legs": [], "visit_cards": []},
            )["visit_cards"].append(attached_visit)

        return OrderedDict(sorted(grouped.items()))


class AttachedTransitLeg(models.Model):
    itinerary = models.ForeignKey(
        Itinerary,
        on_delete=models.CASCADE,
        related_name="attached_transit_legs",
    )
    transit_leg = models.ForeignKey(
        TransitLeg,
        on_delete=models.PROTECT,
        related_name="attached_itineraries",
    )
    start_date = models.DateField()

    def __str__(self):
        return f"{self.transit_leg} on {self.start_date}"


class AttachedVisitCard(models.Model):
    itinerary = models.ForeignKey(
        Itinerary,
        on_delete=models.CASCADE,
        related_name="attached_visit_cards",
    )
    visit_card = models.ForeignKey(
        VisitCard,
        on_delete=models.PROTECT,
        related_name="attached_itineraries",
    )
    start_date = models.DateField()
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.visit_card} on {self.start_date}"
