import re

from django import template
from django.conf import settings

register = template.Library()

CARD_TRANSFORMS = {
    'card-team': 'c_fill,g_face,h_800,w_600,q_auto,f_auto',
    'card-service': 'c_fill,g_auto,h_1067,w_800,q_auto,f_auto',
    'detail-team': 'c_fill,g_face,h_800,w_600,q_auto,f_auto',
    'detail-service': 'c_fill,g_auto,h_800,w_1200,q_auto,f_auto',
}


@register.filter
def absolute_media_url(url):
    if not url:
        return ''
    if url.startswith(('http://', 'https://')):
        return url
    return f'{settings.SITE_URL.rstrip("/")}{url}'


@register.filter
def fill_media_url(image, variant=''):
    if not image:
        return ''
    url = image.url
    transform = CARD_TRANSFORMS.get(variant, '')
    if transform and 'cloudinary.com' in url and '/upload/' in url:
        if f'/upload/{transform}/' in url:
            return url
        return re.sub(r'/upload/(v\d+/)?', f'/upload/{transform}/\\1', url, count=1)
    return url
