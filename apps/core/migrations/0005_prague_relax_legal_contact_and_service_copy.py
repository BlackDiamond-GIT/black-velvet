from django.db import migrations, models


PHONE = '+420 776 739 466'
WHATSAPP_NUMBER = '420776739466'
WHATSAPP_URL = 'https://wa.me/420776739466'
SALON_ADDRESS = 'Lužická 1416/29, 120 00 Vinohrady'

VIP_COPY = {
    'short_desc': 'Exkluzivní a individuální celotělová péče s plnou pozorností certifikovaného terapeuta za využití prémiových bio olejů.',
    'short_desc_cs': 'Exkluzivní a individuální celotělová péče s plnou pozorností certifikovaného terapeuta za využití prémiových bio olejů.',
    'short_desc_en': 'Exclusive and individualized full-body care with the complete attention of a certified therapist using premium organic oils.',
    'short_desc_ru': 'Эксклюзивный индивидуальный уход за всем телом с полным вниманием сертифицированного терапевта и использованием премиальных био-масел.',
}

WOMEN_COPY = {
    'short_desc': 'Zklidňující regenerační rituál v harmonickém a plně soukromém prostředí, zaměřený na odbourání stresu a hluboké uvolnění svalů.',
    'short_desc_cs': 'Zklidňující regenerační rituál v harmonickém a plně soukromém prostředí, zaměřený na odbourání stresu a hluboké uvolnění svalů.',
    'short_desc_en': 'A soothing regenerative ritual in a harmonious and fully private setting, focused on relieving stress and deeply relaxing the muscles.',
    'short_desc_ru': 'Успокаивающий восстанавливающий ритуал в гармоничной и полностью приватной обстановке, направленный на снятие стресса и глубокое расслабление мышц.',
}


def update_public_content(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    Service = apps.get_model('services', 'Service')
    Post = apps.get_model('blog', 'Post')
    Masseuse = apps.get_model('team', 'Masseuse')

    SiteSettings.objects.all().update(
        phone_primary=PHONE,
        rotation_phone_1=PHONE,
        rotation_phone_2=PHONE,
        rotation_phone_3=PHONE,
        location_phone_1=PHONE,
        whatsapp_number=WHATSAPP_NUMBER,
        whatsapp_url=WHATSAPP_URL,
        address=SALON_ADDRESS,
    )

    Service.objects.filter(slug='vip-masaz').update(**VIP_COPY)
    Service.objects.filter(slug='masaz-pro-zeny').update(**WOMEN_COPY)

    for service in Service.objects.filter(is_active=True):
        changed = []
        for field in ('meta_title', 'meta_title_cs', 'meta_title_en', 'meta_title_ru'):
            value = getattr(service, field, '') or ''
            branded = value.replace('Black Elixir', 'Black Velvet')
            if branded != value:
                setattr(service, field, branded)
                changed.append(field)
        if changed:
            service.save(update_fields=changed)

    public_text_fields = {
        Post: (
            'title', 'title_cs', 'title_en', 'title_ru',
            'excerpt', 'excerpt_cs', 'excerpt_en', 'excerpt_ru',
            'content', 'content_cs', 'content_en', 'content_ru',
            'author_name',
            'meta_title', 'meta_title_cs', 'meta_title_en', 'meta_title_ru',
            'meta_description', 'meta_description_cs', 'meta_description_en', 'meta_description_ru',
        ),
        Masseuse: (
            'bio', 'bio_cs', 'bio_en', 'bio_ru',
            'meta_title', 'meta_title_cs', 'meta_title_en', 'meta_title_ru',
            'meta_description', 'meta_description_cs', 'meta_description_en', 'meta_description_ru',
        ),
    }
    for model, fields in public_text_fields.items():
        queryset = model.objects.filter(is_published=True) if model is Post else model.objects.filter(is_active=True)
        for instance in queryset:
            changed = []
            for field in fields:
                value = getattr(instance, field, '') or ''
                branded = value.replace('Black Elixir', 'Black Velvet')
                if branded != value:
                    setattr(instance, field, branded)
                    changed.append(field)
            if changed:
                instance.save(update_fields=changed)


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        ('core', '0004_whatsapp_number_797'),
        ('services', '0005_deactivate_old_services_add_new'),
        ('team', '0004_alter_masseuse_options_masseuse_age_masseuse_bust_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='address',
            field=models.CharField(default=SALON_ADDRESS, max_length=200, verbose_name='Адреса (студія 1)'),
        ),
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
            field=models.CharField(default=WHATSAPP_NUMBER, help_text='Напр. 420776739466 — для wa.me/', max_length=20, verbose_name='WhatsApp (без + і пробілів)'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='whatsapp_url',
            field=models.URLField(blank=True, default=WHATSAPP_URL, verbose_name='WhatsApp URL'),
        ),
        migrations.RunPython(update_public_content, migrations.RunPython.noop),
    ]
