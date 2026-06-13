"""Add ip_only_hash field to BookingClick."""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0003_bookingclick_is_bot"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookingclick",
            name="ip_only_hash",
            field=models.CharField(
                blank=True,
                db_index=True,
                max_length=64,
                verbose_name="IP-only hash",
            ),
        ),
    ]
