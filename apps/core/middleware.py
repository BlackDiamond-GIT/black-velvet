"""Project middleware."""

from django.http import HttpResponsePermanentRedirect
from django.utils import translation

_ADMIN_LANG_COOKIE = 'admin_lang'
_ALLOWED_ADMIN_LANGS = frozenset(('en', 'uk'))


class CsPrefixRedirectMiddleware:
    """Redirect legacy /cs/… URLs to unprefixed Czech URLs."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path == '/cs' or path.startswith('/cs/'):
            new_path = path[3:] or '/'
            query = request.META.get('QUERY_STRING', '')
            target = f'{new_path}?{query}' if query else new_path
            return HttpResponsePermanentRedirect(target)
        return self.get_response(request)


class AdminLocaleMiddleware:
    """Force Ukrainian (or English via cookie) for Django admin routes."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            lang = request.COOKIES.get(_ADMIN_LANG_COOKIE, 'uk')
            if lang not in _ALLOWED_ADMIN_LANGS:
                lang = 'uk'
            with translation.override(lang):
                response = self.get_response(request)
                translation.deactivate()
                return response
        return self.get_response(request)
