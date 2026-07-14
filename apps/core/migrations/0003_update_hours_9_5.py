# -*- coding: utf-8 -*-
# Sjednocení otevírací doby na existujících řádcích: denně 9:00–5:00 (bez „ráno").
# Model default byl změněn dříve, ale existující produkční řádek nesl starou hodnotu.
from django.db import migrations


def update_hours(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    SiteSettings.objects.all().update(
        hours='Denně od 9:00 do 5:00',
        hours_en='Daily from 9 AM to 5 AM',
        hours_ru='Ежедневно с 9:00 до 5:00',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_contentpage_etiquetterule_guestreview_legacyredirect_and_more'),
    ]

    operations = [
        migrations.RunPython(update_hours, migrations.RunPython.noop),
    ]
