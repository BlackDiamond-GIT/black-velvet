"""Replace the retired number +420 776 739 466 with +420 797 669 633.

The owner retired 776 739 466 (8. 10. 2026). Migration 0005 wrote it into
SiteSettings and as field defaults; this puts 797 669 633 in its place.

Only values that contain the old number are touched, so a number someone set
by hand in the admin survives. Public text in the project's own apps is swept
the same way, in case the number was ever typed into copy.

Separators are preserved: ``+420 776 739 466`` -> ``+420 797 669 633``,
``wa.me/420776739466`` -> ``wa.me/420797669633``.

Idempotent. Reverse is a no-op.
"""

import re

from django.db import migrations, models

PHONE = '+420 797 669 633'
WHATSAPP_NUMBER = '420797669633'
WHATSAPP_URL = 'https://wa.me/420797669633'

# Named back-reference on purpose: ``\1466`` would parse as an octal escape.
_OLD = re.compile(r'776(?P<sep>[ .\-]?)739(?P=sep)466')

_PROJECT_APPS = (
    'core', 'blog', 'pages', 'services', 'team', 'booking', 'reservations',
    'media_library',
)


def _swap(value):
    return _OLD.sub(lambda m: f"797{m['sep']}669{m['sep']}633", value)


def replace_phone(apps, schema_editor):
    for label in _PROJECT_APPS:
        try:
            config = apps.get_app_config(label)
        except LookupError:
            continue
        for model in config.get_models():
            fields = [
                f.name for f in model._meta.get_fields()
                if isinstance(f, (models.CharField, models.TextField))
                and not f.many_to_many and f.concrete
            ]
            if not fields:
                continue
            for obj in model.objects.all():
                changed = []
                for name in fields:
                    value = getattr(obj, name, None)
                    if isinstance(value, str) and _OLD.search(value):
                        setattr(obj, name, _swap(value))
                        changed.append(name)
                if changed:
                    obj.save(update_fields=changed)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_restore_velvet_women_copy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='location_phone_1',
            field=models.CharField(default=PHONE, max_length=30, verbose_name='Телефон (студія 1)'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='phone_primary',
            field=models.CharField(default=PHONE, max_length=30, verbose_name='Основний телефон'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='rotation_phone_1',
            field=models.CharField(default=PHONE, max_length=30, verbose_name='Ротаційний телефон 1'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='rotation_phone_2',
            field=models.CharField(default=PHONE, max_length=30, verbose_name='Ротаційний телефон 2'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='rotation_phone_3',
            field=models.CharField(default=PHONE, max_length=30, verbose_name='Ротаційний телефон 3'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='whatsapp_number',
            field=models.CharField(default=WHATSAPP_NUMBER, help_text='Напр. 420797669633 — для wa.me/', max_length=20, verbose_name='WhatsApp (без + і пробілів)'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='whatsapp_url',
            field=models.URLField(blank=True, default=WHATSAPP_URL, verbose_name='WhatsApp URL'),
        ),
        migrations.RunPython(replace_phone, migrations.RunPython.noop),
    ]
