from django.db import migrations


def deactivate_removed_services(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    Service.objects.filter(
        slug__in=['sportovni-masaz', 'lymfaticka-masaz']
    ).update(is_active=False)


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_multi_currency_and_shifts'),
    ]

    operations = [
        migrations.RunPython(
            deactivate_removed_services,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
