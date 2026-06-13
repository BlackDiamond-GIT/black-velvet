from django.conf import settings
from django.utils.translation import get_language


def absolute_url(request, path=''):
    base = settings.SITE_URL.rstrip('/')
    if not path:
        path = request.path
    if path.startswith('http'):
        return path
    return f'{base}{path}'


def build_hreflang(request):
    """Build hreflang URLs for all language variants of current page."""
    from apps.core.i18n import translate_url_for_language

    urls = {}
    current_lang = get_language()
    for code, _ in settings.LANGUAGES:
        urls[code] = absolute_url(request, translate_url_for_language(request.path, code))
    urls['x-default'] = urls.get(settings.LANGUAGE_CODE, urls.get(current_lang, ''))
    return urls


def get_seo_context(request, title, description, og_image=None, canonical_path=None):
    canonical = absolute_url(request, canonical_path or request.path)
    return {
        'title': title,
        'description': description,
        'canonical': canonical,
        'og_image': og_image or f'{settings.SITE_URL.rstrip("/")}/static/img/og-image.png',
        'og_url': canonical,
    }
