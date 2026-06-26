# Generated manually because Python is not installed in this workspace runtime.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("itineraries", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("latitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("longitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("address", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="EducationCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("rail", "Rail"),
                            ("culture", "Culture"),
                            ("language", "Language"),
                            ("regional-context", "Regional context"),
                        ],
                        max_length=20,
                    ),
                ),
                ("body", models.TextField()),
                (
                    "location",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="education_cards",
                        to="itineraries.location",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VisitCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("suggested_hours", models.DecimalField(decimal_places=2, max_digits=5)),
                ("admission_yen", models.PositiveIntegerField()),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="visit_cards",
                        to="itineraries.location",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TransitLeg",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "mode",
                    models.CharField(
                        choices=[
                            ("train", "Train"),
                            ("shinkansen", "Shinkansen"),
                            ("limited-express", "Limited express"),
                            ("bus", "Bus"),
                        ],
                        max_length=20,
                    ),
                ),
                ("operator", models.CharField(blank=True, max_length=100)),
                ("line_name", models.CharField(blank=True, max_length=100)),
                ("fare_yen", models.PositiveIntegerField()),
                ("duration_days", models.PositiveIntegerField()),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="arriving_transit_legs",
                        to="itineraries.location",
                    ),
                ),
                (
                    "origin",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="departing_transit_legs",
                        to="itineraries.location",
                    ),
                ),
            ],
        ),
    ]
