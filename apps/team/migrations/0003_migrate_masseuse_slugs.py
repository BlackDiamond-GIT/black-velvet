from django.db import migrations


def rename_masseuse_slugs(apps, schema_editor):
    Masseuse = apps.get_model('team', 'Masseuse')
    slug_renames = {
        'elena': 'julia',
        'lucie': 'diana',
        'natalie': 'laura',
        'klara': 'vanessa',
        'sofia': 'ella',
        'anna': 'mira',
    }

    for old_slug, new_slug in slug_renames.items():
        masseuse = Masseuse.objects.filter(slug=old_slug).first()
        if not masseuse:
            continue

        Masseuse.objects.filter(slug=new_slug).exclude(pk=masseuse.pk).delete()
        Masseuse.objects.filter(pk=masseuse.pk).update(slug=new_slug)


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_masseuse_updated_at'),
    ]

    operations = [
        migrations.RunPython(rename_masseuse_slugs, migrations.RunPython.noop),
    ]
