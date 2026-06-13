from urllib.parse import unquote, urlsplit, urlunsplit

from django.urls import NoReverseMatch, Resolver404, resolve, reverse
from django.utils.translation import get_language_from_path, override


def translate_url_for_language(url, lang_code):
    """Translate URL between languages (works with prefix_default_language=False)."""
    parsed = urlsplit(url)
    path = unquote(parsed.path)
    source_lang = get_language_from_path(path)

    try:
        if source_lang:
            with override(source_lang):
                match = resolve(path)
        else:
            match = resolve(path)
    except Resolver404:
        return url

    name = f'{match.namespace}:{match.url_name}' if match.namespace else match.url_name
    with override(lang_code):
        try:
            translated_path = reverse(name, args=match.args, kwargs=match.kwargs)
        except NoReverseMatch:
            return url

    return urlunsplit((parsed.scheme, parsed.netloc, translated_path, parsed.query, parsed.fragment))
