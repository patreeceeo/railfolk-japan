from django.contrib import admin

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
        "duration_days",
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


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ("title", "visibility", "owner", "created_at", "updated_at")
    list_filter = ("visibility",)
    search_fields = ("title", "description", "owner__username")
    filter_horizontal = ("education_cards",)


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


admin.site.register(UserProfile)
