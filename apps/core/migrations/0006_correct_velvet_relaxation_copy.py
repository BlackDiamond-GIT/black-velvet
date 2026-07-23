from django.db import migrations


RELAXATION_COPY = {
    'short_desc': 'Hluboká relaxační masáž celého těla s využitím prémiových bio olejů pro odbourání stresu a psychického napětí.',
    'short_desc_cs': 'Hluboká relaxační masáž celého těla s využitím prémiových bio olejů pro odbourání stresu a psychického napětí.',
    'short_desc_en': 'Deep full-body relaxation massage using premium organic oils to relieve stress and mental tension.',
    'short_desc_ru': 'Глубокий расслабляющий массаж всего тела с использованием премиальных био-масел для снятия стресса и психического напряжения.',
}


def update_relaxation_copy(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    Service.objects.filter(slug='relaxacni-masaz').update(**RELAXATION_COPY)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_prague_relax_legal_contact_and_service_copy'),
    ]

    operations = [
        migrations.RunPython(update_relaxation_copy, migrations.RunPython.noop),
    ]
