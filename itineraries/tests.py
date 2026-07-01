from collections import OrderedDict
from datetime import date
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .models import (
    AttachedTransitLeg,
    AttachedVisitCard,
    EducationCard,
    Itinerary,
    Location,
    TransitLeg,
    UserProfile,
    VisitCard,
)


class HomePageTests(SimpleTestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Railfolk Japan")


class AuthPageTests(TestCase):
    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign in")

    def test_login_authenticates_existing_user(self):
        user = get_user_model().objects.create_user(
            username="patreece",
            password="Stronger-pass-2026",
        )

        response = self.client.post(
            reverse("login"),
            {
                "username": "patreece",
                "password": "Stronger-pass-2026",
            },
        )

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(self.client.session["_auth_user_id"], str(user.id))

    def test_logout_uses_builtin_auth_view(self):
        user = get_user_model().objects.create_user(
            username="patreece",
            password="Stronger-pass-2026",
        )
        self.client.force_login(user)

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_signup_page_loads(self):
        response = self.client.get(reverse("signup"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign up")

    def test_signup_creates_profile_and_signs_user_in(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "patreece",
                "email": "patreece@example.com",
                "password": "Stronger-pass-2026",
            },
        )

        user = get_user_model().objects.get(username="patreece")
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(user.email, "patreece@example.com")
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        self.assertEqual(self.client.session["_auth_user_id"], str(user.id))


class UserModelTests(TestCase):
    def test_avatar_key_is_generated_for_new_users(self):
        user = get_user_model().objects.create_user(
            username="patreece",
            email="patreece@example.com",
        )

        self.assertEqual(len(user.avatar_key), 32)
        self.assertNotIn("patreece", user.avatar_key)
        self.assertNotIn("example", user.avatar_key)

    def test_username_rejects_invalid_characters(self):
        user = get_user_model()(username="bad name", email="bad@example.com")

        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_username_rejects_too_short_values(self):
        user = get_user_model()(username="ab", email="ab@example.com")

        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_username_is_case_insensitive_unique(self):
        get_user_model().objects.create_user(username="Patreece")

        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(username="patreece")


class ItineraryDateHelperTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="patreece")
        self.origin = Location.objects.create(
            name="Tokyo",
            description="Capital city",
            latitude="35.681236",
            longitude="139.767125",
        )
        self.destination = Location.objects.create(
            name="Kanazawa",
            description="Castle town",
            latitude="36.578057",
            longitude="136.648659",
        )
        self.visit_location = Location.objects.create(
            name="Kenrokuen",
            description="Garden",
            latitude="36.561325",
            longitude="136.662549",
        )
        self.transit_leg = TransitLeg.objects.create(
            mode=TransitLeg.Mode.SHINKANSEN,
            origin=self.origin,
            destination=self.destination,
            fare_yen=14000,
            duration_hours=25,
        )
        self.same_day_transit_leg = TransitLeg.objects.create(
            mode=TransitLeg.Mode.TRAIN,
            origin=self.destination,
            destination=self.origin,
            fare_yen=9000,
            duration_hours=3,
        )
        self.visit_card = VisitCard.objects.create(
            location=self.visit_location,
            suggested_hours="2.50",
            admission_yen=320,
        )
        self.itinerary = Itinerary.objects.create(
            title="Hokuriku loop",
            description="A short rail-focused trip.",
            visibility=Itinerary.Visibility.PUBLIC,
            owner=self.user,
        )

    def test_total_duration_returns_none_with_no_dated_items(self):
        self.assertIsNone(self.itinerary.total_duration())

    def test_total_duration_uses_single_visit_date(self):
        AttachedVisitCard.objects.create(
            itinerary=self.itinerary,
            visit_card=self.visit_card,
            start_date=date(2026, 4, 3),
        )

        self.assertEqual(
            self.itinerary.total_duration(),
            (date(2026, 4, 3), date(2026, 4, 3)),
        )

    def test_total_duration_includes_transit_leg_duration(self):
        AttachedTransitLeg.objects.create(
            itinerary=self.itinerary,
            transit_leg=self.transit_leg,
            start_date=date(2026, 4, 3),
        )

        self.assertEqual(
            self.itinerary.total_duration(),
            (date(2026, 4, 3), date(2026, 4, 4)),
        )

    def test_total_duration_uses_earliest_start_and_latest_end_for_overlaps(self):
        AttachedTransitLeg.objects.create(
            itinerary=self.itinerary,
            transit_leg=self.transit_leg,
            start_date=date(2026, 4, 3),
        )
        AttachedVisitCard.objects.create(
            itinerary=self.itinerary,
            visit_card=self.visit_card,
            start_date=date(2026, 4, 2),
        )
        AttachedTransitLeg.objects.create(
            itinerary=self.itinerary,
            transit_leg=self.same_day_transit_leg,
            start_date=date(2026, 4, 4),
        )

        self.assertEqual(
            self.itinerary.total_duration(),
            (date(2026, 4, 2), date(2026, 4, 4)),
        )

    def test_grouped_by_date_returns_empty_ordered_dict_with_no_dated_items(self):
        self.assertEqual(self.itinerary.grouped_by_date(), OrderedDict())

    def test_grouped_by_date_returns_single_visit(self):
        attached_visit = AttachedVisitCard.objects.create(
            itinerary=self.itinerary,
            visit_card=self.visit_card,
            start_date=date(2026, 4, 3),
        )

        self.assertEqual(list(self.itinerary.grouped_by_date().items()), [
            (
                date(2026, 4, 3),
                {"transit_legs": [], "visit_cards": [attached_visit]},
            ),
        ])

    def test_grouped_by_date_orders_dates_and_groups_overlaps(self):
        later_leg = AttachedTransitLeg.objects.create(
            itinerary=self.itinerary,
            transit_leg=self.same_day_transit_leg,
            start_date=date(2026, 4, 4),
        )
        early_visit = AttachedVisitCard.objects.create(
            itinerary=self.itinerary,
            visit_card=self.visit_card,
            start_date=date(2026, 4, 2),
        )
        overlap_leg = AttachedTransitLeg.objects.create(
            itinerary=self.itinerary,
            transit_leg=self.transit_leg,
            start_date=date(2026, 4, 3),
        )
        overlap_visit = AttachedVisitCard.objects.create(
            itinerary=self.itinerary,
            visit_card=self.visit_card,
            start_date=date(2026, 4, 3),
        )

        self.assertEqual(list(self.itinerary.grouped_by_date().items()), [
            (
                date(2026, 4, 2),
                {"transit_legs": [], "visit_cards": [early_visit]},
            ),
            (
                date(2026, 4, 3),
                {"transit_legs": [overlap_leg], "visit_cards": [overlap_visit]},
            ),
            (
                date(2026, 4, 4),
                {"transit_legs": [later_leg], "visit_cards": []},
            ),
        ])


class SeedCommandTests(TestCase):
    def test_seed_creates_required_data_and_is_idempotent(self):
        output = StringIO()
        call_command("seed", stdout=output)

        self.assertIn("Seed data loaded.", output.getvalue())
        self.assertEqual(get_user_model().objects.count(), 3)
        self.assertEqual(UserProfile.objects.count(), 3)
        self.assertEqual(Location.objects.count(), 10)
        self.assertEqual(EducationCard.objects.count(), 10)
        self.assertEqual(VisitCard.objects.count(), 10)
        self.assertEqual(TransitLeg.objects.count(), 11)
        self.assertEqual(Itinerary.objects.count(), 3)
        self.assertEqual(
            Itinerary.objects.filter(visibility=Itinerary.Visibility.PUBLIC).count(),
            3,
        )
        self.assertEqual(AttachedTransitLeg.objects.count(), 11)
        self.assertEqual(AttachedVisitCard.objects.count(), 10)

        counts = {
            "users": get_user_model().objects.count(),
            "profiles": UserProfile.objects.count(),
            "locations": Location.objects.count(),
            "education_cards": EducationCard.objects.count(),
            "visit_cards": VisitCard.objects.count(),
            "transit_legs": TransitLeg.objects.count(),
            "itineraries": Itinerary.objects.count(),
            "attached_legs": AttachedTransitLeg.objects.count(),
            "attached_visits": AttachedVisitCard.objects.count(),
        }

        call_command("seed", stdout=StringIO())

        self.assertEqual(get_user_model().objects.count(), counts["users"])
        self.assertEqual(UserProfile.objects.count(), counts["profiles"])
        self.assertEqual(Location.objects.count(), counts["locations"])
        self.assertEqual(EducationCard.objects.count(), counts["education_cards"])
        self.assertEqual(VisitCard.objects.count(), counts["visit_cards"])
        self.assertEqual(TransitLeg.objects.count(), counts["transit_legs"])
        self.assertEqual(Itinerary.objects.count(), counts["itineraries"])
        self.assertEqual(AttachedTransitLeg.objects.count(), counts["attached_legs"])
        self.assertEqual(AttachedVisitCard.objects.count(), counts["attached_visits"])
