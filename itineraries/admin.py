from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.apps import apps
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Count

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


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0


User = get_user_model()

try:
    admin.site.unregister(User)
except NotRegistered:
    pass


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    inlines = (UserProfileInline,)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude", "address")
    search_fields = ("name", "address")


@admin.register(TransitLeg)
class TransitLegAdmin(admin.ModelAdmin):
    list_display = (
        "origin",
        "destination",
        "mode",
        "operator",
        "line_name",
        "fare_yen",
        "duration_hours",
    )
    list_filter = ("mode",)
    search_fields = (
        "origin__name",
        "destination__name",
        "operator",
        "line_name",
    )


@admin.register(VisitCard)
class VisitCardAdmin(admin.ModelAdmin):
    list_display = ("location", "suggested_hours", "admission_yen")
    search_fields = ("location__name",)


@admin.register(EducationCard)
class EducationCardAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "location")
    list_filter = ("category",)
    search_fields = ("title", "body", "location__name")


class AttachedTransitLegInline(admin.TabularInline):
    model = AttachedTransitLeg
    extra = 0
    autocomplete_fields = ("transit_leg",)


class AttachedVisitCardInline(admin.TabularInline):
    model = AttachedVisitCard
    extra = 0
    autocomplete_fields = ("visit_card",)


class ItineraryEducationCardInline(admin.TabularInline):
    model = Itinerary.education_cards.through
    extra = 0
    autocomplete_fields = ("educationcard",)
    verbose_name = "education card"
    verbose_name_plural = "education cards"


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    change_form_template = "admin/itineraries/itinerary/change_form.html"
    exclude = ("education_cards",)
    inlines = (
        AttachedTransitLegInline,
        AttachedVisitCardInline,
        ItineraryEducationCardInline,
    )
    list_display = ("title", "visibility", "owner", "created_at", "updated_at")
    list_filter = ("visibility",)
    search_fields = ("title", "description", "owner__username")

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["vote_reason_counts"] = self.get_vote_reason_counts(object_id)
        extra_context["vote_reason_counts_available"] = self.vote_model_exists()
        return super().change_view(request, object_id, form_url, extra_context)

    def vote_model_exists(self):
        try:
            apps.get_model("itineraries", "Vote")
        except LookupError:
            return False

        return True

    def get_vote_reason_counts(self, itinerary_id):
        try:
            Vote = apps.get_model("itineraries", "Vote")
            reasons_field = Vote._meta.get_field("reasons")
        except LookupError:
            return []

        if reasons_field.many_to_many:
            reason_name_field = self.get_reason_name_field(reasons_field.remote_field.model)
            reason_lookup = f"reasons__{reason_name_field}"
            rows = (
                Vote.objects.filter(itinerary_id=itinerary_id)
                .values("direction", reason_lookup)
                .annotate(count=Count("id"))
                .order_by("direction", reason_lookup)
            )

            return [
                {
                    "direction": row["direction"],
                    "reason": row[reason_lookup],
                    "count": row["count"],
                }
                for row in rows
            ]

        return self.get_json_reason_counts(Vote, itinerary_id)

    def get_reason_name_field(self, reason_model):
        for field_name in ("label", "name", "title", "slug", "code"):
            try:
                reason_model._meta.get_field(field_name)
            except FieldDoesNotExist:
                continue

            return field_name

        return reason_model._meta.pk.name

    def get_json_reason_counts(self, Vote, itinerary_id):
        counts = {}

        for direction, reasons in Vote.objects.filter(itinerary_id=itinerary_id).values_list(
            "direction",
            "reasons",
        ):
            for reason in reasons or []:
                key = (direction, reason)
                counts[key] = counts.get(key, 0) + 1

        return [
            {"direction": direction, "reason": reason, "count": count}
            for (direction, reason), count in sorted(counts.items())
        ]


@admin.register(AttachedTransitLeg)
class AttachedTransitLegAdmin(admin.ModelAdmin):
    list_display = ("itinerary", "transit_leg", "start_date")
    search_fields = (
        "itinerary__title",
        "transit_leg__origin__name",
        "transit_leg__destination__name",
    )


@admin.register(AttachedVisitCard)
class AttachedVisitCardAdmin(admin.ModelAdmin):
    list_display = ("itinerary", "visit_card", "start_date")
    search_fields = ("itinerary__title", "visit_card__location__name", "note")


try:
    Vote = apps.get_model("itineraries", "Vote")
except LookupError:
    Vote = None

if Vote is not None:
    admin.site.register(Vote)
