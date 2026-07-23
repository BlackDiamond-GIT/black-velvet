from django.db import migrations


WOMEN_COPY = {
    'short_desc': 'Speciální masáž přizpůsobená potřebám ženského těla pro hlubokou relaxaci a harmonii.',
    'short_desc_cs': 'Speciální masáž přizpůsobená potřebám ženského těla pro hlubokou relaxaci a harmonii.',
    'short_desc_en': 'Special massage tailored to the needs of the female body for deep relaxation and harmony.',
    'short_desc_ru': 'Специальный массаж, адаптированный к потребностям женского тела для глубокого расслабления и гармонии.',
}


def restore_women_copy(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    Service.objects.filter(slug='masaz-pro-zeny').update(**WOMEN_COPY)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_correct_velvet_relaxation_copy'),
    ]

    operations = [
        migrations.RunPython(restore_women_copy, migrations.RunPython.noop),
    ]
