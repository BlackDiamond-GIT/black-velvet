from django.db import migrations


def rename_masseuse_slugs(apps, schema_editor):
    from apps.core.seed_loader import migrate_masseuse_slugs

    migrate_masseuse_slugs()


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_masseuse_updated_at'),
    ]

    operations = [
        migrations.RunPython(rename_masseuse_slugs, migrations.RunPython.noop),
    ]
