from datetime import date, time, timedelta

from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.blog.models import Post, Tag
from apps.core.seed_loader import (
    load_bundle,
    masseuse_defaults,
    model_defaults,
    seed_media_path,
    service_defaults,
    TRANSLATED_FIELDS,
)
from apps.pages.models import FAQ, PriceCategory, PriceItem, Review
from apps.reservations.models import TimeSlot
from apps.services.models import Service
from apps.team.models import Masseuse


class Command(BaseCommand):
    help = 'Seed initial Black Velvet data from bundled JSON'

    def handle(self, *args, **options):
        bundle = load_bundle()
        service_map = self._import_services(bundle['services'])
        masseuse_map = self._import_masseuses(bundle['masseuses'], bundle['masseuse_services'], service_map)
        tag_map = self._import_tags(bundle['tags'])
        self._import_posts(bundle['posts'], bundle['post_tags'], tag_map)
        self._import_faqs(bundle['faqs'])
        self._import_reviews(bundle['reviews'])
        self._import_prices(bundle['price_categories'], bundle['price_items'])
        self._import_timeslots(masseuse_map.values())

        self.stdout.write(self.style.SUCCESS('Seed data loaded successfully.'))

    def _attach_image(self, instance, field_name, category, slug, dest_name):
        src = seed_media_path(category, slug)
        if not src:
            self.stdout.write(self.style.WARNING(f'Seed image missing: {category}/{slug}'))
            return

        field = getattr(instance, field_name)
        if field and field.name:
            if field.url.startswith('https://res.cloudinary.com/'):
                return
            field.delete(save=False)

        storage_name = f'black-velvet/{category}/{slug}.webp'
        with src.open('rb') as handle:
            field.save(storage_name, File(handle), save=True)

    def _import_services(self, rows):
        service_map = {}
        for row in rows:
            service, _ = Service.objects.update_or_create(
                slug=row['slug'],
                defaults=service_defaults(row),
            )
            self._attach_image(
                service,
                'image',
                'services',
                row['slug'],
                f"{row['slug']}.webp",
            )
            service_map[row['id']] = service
        return service_map

    def _import_masseuses(self, rows, links, service_map):
        masseuse_map = {}
        for row in rows:
            masseuse, _ = Masseuse.objects.update_or_create(
                slug=row['slug'],
                defaults=masseuse_defaults(row),
            )
            self._attach_image(
                masseuse,
                'photo',
                'team',
                row['slug'],
                f"{row['slug']}.webp",
            )
            masseuse_map[row['id']] = masseuse

        for link in links:
            masseuse = masseuse_map.get(link['masseuse_id'])
            service = service_map.get(link['service_id'])
            if masseuse and service:
                masseuse.services.add(service)

        return masseuse_map

    def _import_tags(self, rows):
        tag_map = {}
        for row in rows:
            tag, _ = Tag.objects.update_or_create(
                slug=row['slug'],
                defaults=model_defaults(row, TRANSLATED_FIELDS['tags']),
            )
            tag_map[row['id']] = tag
        return tag_map

    def _import_posts(self, rows, links, tag_map):
        post_tag_ids = {}
        for link in links:
            post_tag_ids.setdefault(link['post_id'], []).append(link['tag_id'])

        for row in rows:
            defaults = model_defaults(row, TRANSLATED_FIELDS['posts'])
            defaults.update({
                'author_name': row.get('author_name') or 'Black Velvet',
                'published_at': row.get('published_at') or timezone.now(),
                'is_published': bool(row.get('is_published', True)),
            })
            post, _ = Post.objects.update_or_create(
                slug=row['slug'],
                defaults=defaults,
            )
            self._attach_image(
                post,
                'image',
                'blog',
                row['slug'],
                f"{row['slug']}.webp",
            )
            tag_ids = post_tag_ids.get(row['id'], [])
            post.tags.set([tag_map[tag_id] for tag_id in tag_ids if tag_id in tag_map])

    def _import_faqs(self, rows):
        for row in rows:
            defaults = model_defaults(row, TRANSLATED_FIELDS['faqs'])
            defaults.update({
                'page': row.get('page') or FAQ.PAGE_HOME,
                'order': row.get('order', 0),
                'is_active': bool(row.get('is_active', True)),
            })
            FAQ.objects.update_or_create(
                question=row['question'],
                defaults=defaults,
            )

    def _import_reviews(self, rows):
        for row in rows:
            defaults = model_defaults(row, TRANSLATED_FIELDS['reviews'])
            defaults.update({
                'rating': row.get('rating', 5),
                'is_published': bool(row.get('is_published', True)),
                'order': row.get('order', 0),
            })
            Review.objects.update_or_create(
                author=row['author'],
                defaults=defaults,
            )

    def _import_prices(self, categories, items):
        category_map = {}
        for row in categories:
            category, _ = PriceCategory.objects.update_or_create(
                name=row['name'],
                defaults={
                    **model_defaults(row, TRANSLATED_FIELDS['price_categories']),
                    'order': row.get('order', 0),
                },
            )
            category_map[row['id']] = category

        for category in category_map.values():
            category.items.all().delete()

        for row in items:
            category = category_map.get(row['category_id'])
            if not category:
                continue
            PriceItem.objects.create(
                category=category,
                **model_defaults(row, TRANSLATED_FIELDS['price_items']),
                duration=row['duration'],
                price=row['price'],
                order=row.get('order', 0),
            )

    def _import_timeslots(self, masseuses):
        today = date.today()
        times = [time(hour, 0) for hour in range(10, 20)]
        for day_offset in range(1, 15):
            slot_date = today + timedelta(days=day_offset)
            for masseuse in masseuses:
                for slot_time in times:
                    TimeSlot.objects.get_or_create(
                        masseuse=masseuse,
                        date=slot_date,
                        time=slot_time,
                        defaults={'is_booked': False},
                    )
