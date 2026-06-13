from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.blog.models import Post, Tag
from apps.core.velvet_loader import (
    OLD_BLOG_SLUGS,
    ensure_velvet_root,
    load_blog_posts,
    load_masseuses,
    load_services,
    velvet_image_path,
)
from apps.pages.models import PriceCategory, PriceItem
from apps.services.models import Service
from apps.team.models import Masseuse


class Command(BaseCommand):
    help = 'Import masseuses, services and blog content from Black Velvet project'

    def handle(self, *args, **options):
        ensure_velvet_root()
        media_root = Path(settings.MEDIA_ROOT)
        (media_root / 'team').mkdir(parents=True, exist_ok=True)
        (media_root / 'services').mkdir(parents=True, exist_ok=True)
        (media_root / 'blog').mkdir(parents=True, exist_ok=True)

        self._import_services(media_root)
        self._import_masseuses(media_root)
        self._import_blog(media_root)
        self._sync_prices()

        self.stdout.write(self.style.SUCCESS('Velvet content imported successfully.'))

    def _attach_image(self, instance, field_name, src_path, dest_subdir, dest_name):
        if not src_path.is_file():
            self.stdout.write(self.style.WARNING(f'Image missing: {src_path}'))
            return
        current = getattr(instance, field_name)
        if current:
            current.delete(save=False)
        with src_path.open('rb') as handle:
            getattr(instance, field_name).save(dest_name, File(handle), save=True)

    def _import_services(self, media_root):
        for item in load_services():
            service, _ = Service.objects.update_or_create(
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
                    'duration_min': item['duration'],
                    'duration_max': item['duration'],
                    'price_czk': item['price_czk'],
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
            service.price_label = f'od {service.price_czk} Kč'
            service.save(update_fields=['price_label'])

            src = velvet_image_path('services', item['velvet_slug'])
            dest_name = f"{item['slug']}.webp"
            self._attach_image(service, 'image', src, 'services', dest_name)
            self.stdout.write(f'Service: {service.name}')

    def _import_masseuses(self, media_root):
        for item in load_masseuses():
            masseuse, _ = Masseuse.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'name': item['name'],
                    'bio': item['bio_cs'],
                    'bio_en': item['bio_en'],
                    'bio_ru': item['bio_ru'],
                    'specializations': item['specializations_cs'],
                    'specializations_en': item['specializations_en'],
                    'specializations_ru': item['specializations_ru'],
                    'years_experience': item['years_experience'],
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

            src = velvet_image_path('masseuses', item['velvet_slug'])
            dest_name = f"{item['slug']}.webp"
            self._attach_image(masseuse, 'photo', src, 'team', dest_name)
            self.stdout.write(f'Masseuse: {masseuse.name}')

    def _import_blog(self, media_root):
        Post.objects.filter(slug__in=OLD_BLOG_SLUGS).delete()

        tags = {}
        for name in ['Zdraví', 'Tipy', 'Masáže']:
            tag, _ = Tag.objects.get_or_create(name=name, defaults={'slug': name.lower()})
            tags[name] = tag

        tag_map = {
            'koristi-masazu-pro-zdorovi': tags['Zdraví'],
            'relaks-meditace-masaz': tags['Tipy'],
            'spa-retreat-kompletni-pruvodce': tags['Masáže'],
        }

        for i, item in enumerate(load_blog_posts()):
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

            src = velvet_image_path('blog', item['slug'])
            dest_name = f"{item['slug']}.webp"
            self._attach_image(post, 'image', src, 'blog', dest_name)
            self.stdout.write(f'Blog post: {post.title}')

    def _sync_prices(self):
        cat, _ = PriceCategory.objects.get_or_create(name='Masáže', defaults={'order': 0})
        PriceItem.objects.filter(category=cat).delete()
        for i, svc in enumerate(Service.objects.filter(is_active=True).order_by('order', 'name')):
            PriceItem.objects.create(
                category=cat,
                service_name=svc.name,
                duration=svc.duration_display,
                price=svc.price_label,
                order=i,
            )
