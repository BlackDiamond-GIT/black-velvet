from django.conf import settings
from django.db.models import Avg, Count

from .seo import build_hreflang

_OG_LOCALE_MAP = {
    'cs': 'cs_CZ',
    'en': 'en_US',
    'ru': 'ru_RU',
}


def _social_urls():
    from .models import SiteSettings

    site = SiteSettings.load()
    return {
        'SITE_INSTAGRAM': site.instagram_url or settings.SITE_INSTAGRAM,
        'SITE_FACEBOOK': site.facebook_url or settings.SITE_FACEBOOK,
        'SITE_WHATSAPP_URL': site.whatsapp_url or settings.SITE_WHATSAPP,
    }


def site_settings(request):
    from apps.pages.models import Review
    aggregate = Review.objects.filter(is_published=True).aggregate(
        avg=Avg('rating'), count=Count('id')
    )
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_URL': settings.SITE_URL,
        'SITE_PHONE': settings.SITE_PHONE,
        'SITE_EMAIL': settings.SITE_EMAIL,
        'SITE_ADDRESS': settings.SITE_ADDRESS,
        'SITE_STREET': settings.SITE_STREET,
        'SITE_CITY': settings.SITE_CITY,
        'SITE_POSTAL': settings.SITE_POSTAL,
        'SITE_COUNTRY': settings.SITE_COUNTRY,
        'SITE_LAT': settings.SITE_LAT,
        'SITE_LNG': settings.SITE_LNG,
        **_social_urls(),
        'GA4_MEASUREMENT_ID': settings.GA4_MEASUREMENT_ID,
        'REVIEW_RATING': round(aggregate['avg'] or 0, 1),
        'REVIEW_COUNT': aggregate['count'] or 0,
    }


def hreflang(request):
    from django.utils.translation import get_language
    urls = build_hreflang(request)
    lang = (get_language() or settings.LANGUAGE_CODE)[:2]
    return {
        'hreflang_urls': urls,
        'hreflang_default': urls.get('x-default', ''),
        'OG_LOCALE': _OG_LOCALE_MAP.get(lang, 'cs_CZ'),
    }
