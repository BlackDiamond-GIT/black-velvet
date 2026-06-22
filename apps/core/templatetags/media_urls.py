from django import template
from django.conf import settings

from apps.media_library.cloudinary_urls import apply_cloudinary_transform, normalize_cloudinary_url

register = template.Library()

CARD_TRANSFORMS = {
    'card-team': 'c_fill,g_face,h_800,w_600,q_auto,f_auto',
    'card-service': 'c_fill,g_auto,h_1067,w_800,q_auto,f_auto',
    'detail-team': 'c_fill,g_face,h_800,w_600,q_auto,f_auto',
    'detail-service': 'c_fill,g_auto,h_800,w_1200,q_auto,f_auto',
}


def _image_url(image) -> str:
    if not image:
        return ''
    if hasattr(image, 'secure_url'):
        url = image.secure_url
    elif hasattr(image, 'url'):
        url = image.url
    elif isinstance(image, str):
        url = image
    else:
        return ''
    return normalize_cloudinary_url(url or '')


@register.filter
def absolute_media_url(url):
    if not url:
        return ''
    url = normalize_cloudinary_url(url)
    if url.startswith(('http://', 'https://')):
        return url
    return f'{settings.SITE_URL.rstrip("/")}{url}'


@register.filter
def fill_media_url(image, variant=''):
    url = _image_url(image)
    if not url:
        return ''
    transform = CARD_TRANSFORMS.get(variant, '')
    if transform and 'cloudinary.com' in url and '/upload/' in url:
        if f'/upload/{transform}/' in url:
            return url
        return apply_cloudinary_transform(url, transform)
    return url
