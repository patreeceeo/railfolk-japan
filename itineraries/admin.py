from django.contrib import admin

from .models import EducationCard, Location, TransitLeg, UserProfile, VisitCard


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


admin.site.register(UserProfile)
