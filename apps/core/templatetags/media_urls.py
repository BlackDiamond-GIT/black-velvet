from django import template
from django.conf import settings

register = template.Library()


@register.filter
def absolute_media_url(url):
    if not url:
        return ''
    if url.startswith(('http://', 'https://')):
        return url
    return f'{settings.SITE_URL.rstrip("/")}{url}'
