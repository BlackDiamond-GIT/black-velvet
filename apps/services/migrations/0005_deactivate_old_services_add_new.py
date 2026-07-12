from django.db import migrations


def deactivate_old_services(apps, schema_editor):
    """Deactivate the 3 old services that are not being repurposed by the seed upsert.
    'relaxacni-masaz' is intentionally omitted: the seed will overwrite that row
    in-place with the new 'Relaxační masáž' service definition.
    """
    Service = apps.get_model('services', 'Service')
    Service.objects.filter(
        slug__in=['aromaterapeuticka-masaz', 'klasicka-masaz', 'relax-masaz']
    ).update(is_active=False)


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_deactivate_removed_services'),
    ]

    operations = [
        migrations.RunPython(
            deactivate_old_services,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
