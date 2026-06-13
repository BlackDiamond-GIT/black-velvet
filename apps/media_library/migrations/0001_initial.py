from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CloudinaryImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("public_id", models.CharField(db_index=True, max_length=255, unique=True, verbose_name="Cloudinary public_id")),
                ("secure_url", models.URLField(max_length=500, verbose_name="Secure URL")),
                ("title", models.CharField(blank=True, max_length=200, verbose_name="Title / label")),
                ("width", models.PositiveIntegerField(blank=True, null=True, verbose_name="Width (px)")),
                ("height", models.PositiveIntegerField(blank=True, null=True, verbose_name="Height (px)")),
                ("format", models.CharField(blank=True, max_length=10, verbose_name="Format")),
                ("bytes", models.PositiveIntegerField(blank=True, null=True, verbose_name="File size (bytes)")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True, verbose_name="Uploaded at")),
            ],
            options={
                "verbose_name": "Cloudinary Image",
                "verbose_name_plural": "Cloudinary Images",
                "ordering": ["-uploaded_at"],
            },
        ),
    ]
