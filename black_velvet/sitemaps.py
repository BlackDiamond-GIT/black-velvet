from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.blog.models import Post
from apps.services.models import Service
from apps.team.models import Masseuse


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    alternates = True
    x_default = True

    def items(self):
        return [
            ('core:home', 1.0),
            ('services:list', 0.8),
            ('team:list', 0.7),
            ('pages:schedule', 0.7),
            ('pages:prices', 0.8),
            ('blog:list', 0.6),
            ('pages:contact', 0.8),
            ('reservations:wizard', 0.8),
            ('pages:about', 0.6),
            ('pages:salon_rules', 0.5),
            ('pages:privacy', 0.5),
        ]

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]


class ServiceSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    alternates = True
    x_default = True

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class TeamSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    alternates = True
    x_default = True

    def items(self):
        return Masseuse.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6
    alternates = True
    x_default = True

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


SITEMAPS = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'team': TeamSitemap,
    'blog': BlogSitemap,
}
