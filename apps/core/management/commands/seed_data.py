from datetime import date, time, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.blog.models import Post, Tag
from apps.core.velvet_loader import (
    OLD_BLOG_SLUGS,
    ensure_velvet_root,
    load_blog_posts,
    load_masseuses,
    load_services,
)
from apps.pages.models import FAQ, PriceCategory, PriceItem, Review
from apps.reservations.models import TimeSlot
from apps.services.models import Service
from apps.team.models import Masseuse


class Command(BaseCommand):
    help = 'Seed initial Black Velvet data'

    def handle(self, *args, **options):
        ensure_velvet_root()

        for item in load_services():
            Service.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'name': item['name_cs'],
                    'name_en': item['name_en'],
                    'name_ru': item['name_ru'],
                    'short_desc': item['short_desc_cs'],
                    'short_desc_en': item['short_desc_en'],
                    'short_desc_ru': item['short_desc_ru'],
                    'description': item['description_cs'],
                    'description_en': item['description_en'],
                    'description_ru': item['description_ru'],
                    'price_czk': item['price_czk'],
                    'duration_min': item['duration'],
                    'duration_max': item['duration'],
                    'meta_title': item['meta_title_cs'],
                    'meta_title_en': item['meta_title_en'],
                    'meta_title_ru': item['meta_title_ru'],
                    'meta_description': item['meta_description_cs'],
                    'meta_description_en': item['meta_description_en'],
                    'meta_description_ru': item['meta_description_ru'],
                    'order': item['order'] - 1,
                    'is_active': True,
                },
            )

        for item in load_masseuses():
            masseuse, _ = Masseuse.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'name': item['name'],
                    'specializations': item['specializations_cs'],
                    'specializations_en': item['specializations_en'],
                    'specializations_ru': item['specializations_ru'],
                    'years_experience': item['years_experience'],
                    'bio': item['bio_cs'],
                    'bio_en': item['bio_en'],
                    'bio_ru': item['bio_ru'],
                    'meta_title': item['meta_title_cs'],
                    'meta_title_en': item['meta_title_en'],
                    'meta_title_ru': item['meta_title_ru'],
                    'meta_description': item['meta_description_cs'],
                    'meta_description_en': item['meta_description_en'],
                    'meta_description_ru': item['meta_description_ru'],
                    'order': item['order'],
                    'is_active': True,
                },
            )
            services = Service.objects.filter(slug__in=item['service_slugs'])
            masseuse.services.set(services)

        faqs = [
            {
                'question': 'Jak dlouho trvá masáž?',
                'question_en': 'How long does a massage last?',
                'question_ru': 'Сколько длится массаж?',
                'answer': 'Nabízíme masáže v délce 30, 60 nebo 90 minut. Doporučujeme vyhradit si navíc 15 minut na přípravu.',
                'answer_en': 'We offer massages lasting 30, 60 or 90 minutes. We recommend allowing an extra 15 minutes for preparation.',
                'answer_ru': 'Мы предлагаем массаж продолжительностью 30, 60 или 90 минут. Рекомендуем заложить дополнительно 15 минут на подготовку.',
            },
            {
                'question': 'Co si mám přinést na masáž?',
                'question_en': 'What should I bring to a massage?',
                'question_ru': 'Что нужно взять с собой на массаж?',
                'answer': 'Vše potřebné zajistíme — prémiové ručníky, masážní oleje a jednorázové prádlo.',
                'answer_en': 'We provide everything you need — premium towels, massage oils and disposable linens.',
                'answer_ru': 'Мы предоставляем всё необходимое — премиальные полотенца, массажные масла и одноразовое бельё.',
            },
            {
                'question': 'Jak probíhá rezervace?',
                'question_en': 'How does booking work?',
                'question_ru': 'Как проходит бронирование?',
                'answer': 'Rezervaci provedete online nebo telefonicky. Potvrzení obdržíte emailem do 30 minut.',
                'answer_en': 'You can book online or by phone. Confirmation will be sent by email within 30 minutes.',
                'answer_ru': 'Записаться можно онлайн или по телефону. Подтверждение придёт на email в течение 30 минут.',
            },
            {
                'question': 'Mohu zrušit nebo změnit rezervaci?',
                'question_en': 'Can I cancel or change my booking?',
                'question_ru': 'Можно ли отменить или изменить бронирование?',
                'answer': 'Zrušení je zdarma nejpozději 24 hodin před termínem.',
                'answer_en': 'Cancellation is free up to 24 hours before the appointment.',
                'answer_ru': 'Отмена бесплатна не позднее чем за 24 часа до записи.',
            },
            {
                'question': 'Nabízíte dárkové poukazy?',
                'question_en': 'Do you offer gift vouchers?',
                'question_ru': 'Предлагаете ли вы подарочные сертификаты?',
                'answer': 'Ano, vydáváme dárkové poukazy na libovolnou masáž nebo částku.',
                'answer_en': 'Yes, we issue gift vouchers for any massage or amount.',
                'answer_ru': 'Да, мы выпускаем подарочные сертификаты на любой массаж или сумму.',
            },
        ]
        for i, item in enumerate(faqs):
            FAQ.objects.update_or_create(
                question=item['question'],
                defaults={
                    'question_en': item['question_en'],
                    'question_ru': item['question_ru'],
                    'answer': item['answer'],
                    'answer_en': item['answer_en'],
                    'answer_ru': item['answer_ru'],
                    'page': FAQ.PAGE_HOME,
                    'order': i,
                },
            )

        reviews = [
            (
                'Markéta V.',
                'Stálá klientka',
                'Regular client',
                'Постоянная клиентка',
                'Nádherná zkušenost. Prostředí salonu je naprosto unikátní a masérka Julia byla profesionální.',
                'A wonderful experience. The salon atmosphere is truly unique and masseuse Julia was professional.',
                'Прекрасный опыт. Атмосфера салона по-настоящему уникальна, а массажистка Юлия была профессиональной.',
                5,
            ),
            (
                'Tomáš K.',
                'Pravidelný host',
                'Regular guest',
                'Постоянный гость',
                'Sportovní masáž u Diany mi pomohla po závodě. Salon má fantastickou atmosféru.',
                'Sports massage with Diana helped me after a race. The salon has a fantastic atmosphere.',
                'Спортивный массаж у Дианы помог после соревнований. В салоне фантастическая атмосфера.',
                5,
            ),
            (
                'Alena P.',
                'Klientka',
                'Client',
                'Клиентка',
                'Rezervace proběhla hladce. Aromamasáž překonala má očekávání.',
                'Booking went smoothly. The aromatherapy massage exceeded my expectations.',
                'Бронирование прошло гладко. Аромамассаж превзошёл мои ожидания.',
                5,
            ),
        ]
        for i, (author, role, role_en, role_ru, text, text_en, text_ru, rating) in enumerate(reviews):
            Review.objects.update_or_create(
                author=author,
                defaults={
                    'role': role,
                    'role_en': role_en,
                    'role_ru': role_ru,
                    'text': text,
                    'text_en': text_en,
                    'text_ru': text_ru,
                    'rating': rating,
                    'order': i,
                },
            )

        cat, _ = PriceCategory.objects.update_or_create(
            name='Masáže',
            defaults={
                'name_en': 'Massages',
                'name_ru': 'Массаж',
                'order': 0,
            },
        )
        PriceItem.objects.filter(category=cat).delete()
        for i, svc in enumerate(Service.objects.filter(is_active=True).order_by('order', 'name')):
            PriceItem.objects.create(
                category=cat,
                service_name=svc.name,
                service_name_en=svc.name_en,
                service_name_ru=svc.name_ru,
                duration=svc.duration_display,
                price=svc.price_label,
                order=i,
            )

        tags = {}
        tag_data = [
            ('Zdraví', 'Health', 'Здоровье', 'zdravi'),
            ('Tipy', 'Tips', 'Советы', 'tipy'),
            ('Masáže', 'Massages', 'Массаж', 'masaze'),
            ('Aromaterapie', 'Aromatherapy', 'Ароматерапия', 'aromaterapie'),
        ]
        for name_cs, name_en, name_ru, slug in tag_data:
            tag, _ = Tag.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': name_cs,
                    'name_en': name_en,
                    'name_ru': name_ru,
                },
            )
            tags[name_cs] = tag

        Post.objects.filter(slug__in=OLD_BLOG_SLUGS).delete()

        tag_map = {
            'koristi-masazu-pro-zdorovi': tags['Zdraví'],
            'relaks-meditace-masaz': tags['Tipy'],
            'spa-retreat-kompletni-pruvodce': tags['Masáže'],
        }

        for item in load_blog_posts():
            post, created = Post.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'title': item['title_cs'],
                    'title_en': item['title_en'],
                    'title_ru': item['title_ru'],
                    'excerpt': item['excerpt_cs'],
                    'excerpt_en': item['excerpt_en'],
                    'excerpt_ru': item['excerpt_ru'],
                    'content': item['content_cs'],
                    'content_en': item['content_en'],
                    'content_ru': item['content_ru'],
                    'author_name': 'Black Velvet',
                    'published_at': timezone.now(),
                    'is_published': True,
                },
            )
            if created:
                post.tags.set([tag_map[item['slug']]])

        today = date.today()
        masseuses = list(Masseuse.objects.all())
        times = [time(h, 0) for h in range(10, 20)]
        for day_offset in range(1, 15):
            d = today + timedelta(days=day_offset)
            for masseuse in masseuses:
                for t in times:
                    TimeSlot.objects.get_or_create(
                        masseuse=masseuse,
                        date=d,
                        time=t,
                        defaults={'is_booked': False},
                    )

        self.stdout.write(self.style.SUCCESS('Seed data loaded successfully.'))
