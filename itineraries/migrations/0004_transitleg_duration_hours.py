from django.db import migrations


def convert_days_to_hours(apps, schema_editor):
    TransitLeg = apps.get_model("itineraries", "TransitLeg")

    for transit_leg in TransitLeg.objects.all():
        transit_leg.duration_hours *= 24
        transit_leg.save(update_fields=["duration_hours"])


def convert_hours_to_days(apps, schema_editor):
    TransitLeg = apps.get_model("itineraries", "TransitLeg")

    for transit_leg in TransitLeg.objects.all():
        transit_leg.duration_hours = max(1, transit_leg.duration_hours // 24)
        transit_leg.save(update_fields=["duration_hours"])


class Migration(migrations.Migration):
    dependencies = [
        ("itineraries", "0003_itinerary_attachedvisitcard_attachedtransitleg"),
    ]

    operations = [
        migrations.RenameField(
            model_name="transitleg",
            old_name="duration_days",
            new_name="duration_hours",
        ),
        migrations.RunPython(convert_days_to_hours, convert_hours_to_days),
    ]
