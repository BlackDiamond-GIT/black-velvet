from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def crumb(name, url_name=None, url_kwargs=None):
    item = {'name': name}
    if url_name:
        item['url'] = reverse(url_name, kwargs=url_kwargs or {})
    return item


def home_crumb():
    return crumb(_('Domů'), 'core:home')
