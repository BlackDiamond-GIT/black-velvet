"""BookingClick model for server-side WhatsApp/reservation click counts."""

from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BookingClick",
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
                    "clicked_at",
                    models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Clicked at"),
                ),
                (
                    "channel",
                    models.CharField(db_index=True, max_length=16, verbose_name="Channel"),
                ),
                (
                    "placement",
                    models.CharField(db_index=True, max_length=40, verbose_name="Placement"),
                ),
                (
                    "page_path",
                    models.CharField(blank=True, max_length=300, verbose_name="Page path"),
                ),
                ("lang", models.CharField(blank=True, max_length=5, verbose_name="Language")),
                (
                    "masseuse_slug",
                    models.CharField(blank=True, max_length=100, verbose_name="Masseuse slug"),
                ),
                (
                    "service_slug",
                    models.CharField(blank=True, max_length=100, verbose_name="Service slug"),
                ),
                (
                    "duration_min",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Duration (min)",
                    ),
                ),
                (
                    "ip_hash",
                    models.CharField(blank=True, max_length=64, verbose_name="IP hash"),
                ),
            ],
            options={
                "verbose_name": "Booking click",
                "verbose_name_plural": "Booking clicks",
                "ordering": ("-clicked_at",),
                "indexes": [
                    models.Index(fields=["clicked_at", "placement"], name="booking_cl_clicked_7a8b2d_idx"),
                ],
            },
        ),
    ]
