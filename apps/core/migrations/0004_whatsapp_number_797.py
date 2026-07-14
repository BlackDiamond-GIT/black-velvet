# -*- coding: utf-8 -*-
"""Sjednotit všechna telefonní/WhatsApp čísla na +420 797 669 633.

Rotace telefonů (rotation_phone_1/2/3) napájela WhatsApp přes
get_active_whatsapp_number, takže wa.me odkazy braly staré číslo 778 622 334.
Model default byl změněn, ale existující produkční řádek si držel staré číslo.
"""
from django.db import migrations

PHONE = '+420 797 669 633'
WA = '420797669633'


def set_numbers(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    SiteSettings.objects.all().update(
        phone_primary=PHONE,
        rotation_phone_1=PHONE,
        rotation_phone_2=PHONE,
        rotation_phone_3=PHONE,
        location_phone_1=PHONE,
        whatsapp_number=WA,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_update_hours_9_5'),
    ]

    operations = [
        migrations.RunPython(set_numbers, migrations.RunPython.noop),
    ]
