"""Add is_bot field to BookingClick."""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0002_bookingclick"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookingclick",
            name="is_bot",
            field=models.BooleanField(db_index=True, default=False, verbose_name="Bot traffic"),
        ),
    ]
