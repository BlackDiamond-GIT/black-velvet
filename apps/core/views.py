from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import check_for_language, gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from apps.pages.models import FAQ, Review
from apps.services.models import Service

from .i18n import translate_url_for_language
from .middleware import _ADMIN_LANG_COOKIE
from .mixins import SEOMixin


@require_POST
def set_language(request):
    """Switch site language and redirect to the equivalent page URL."""
    next_url = request.POST.get('next', request.GET.get('next', '/'))
    if not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = request.META.get('HTTP_REFERER', '/')
        if not url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            next_url = '/'

    lang_code = request.POST.get('language')
    if lang_code and check_for_language(lang_code):
        translated = translate_url_for_language(next_url, lang_code)
        if translated != next_url:
            next_url = translated

    response = HttpResponseRedirect(next_url)
    if lang_code and check_for_language(lang_code):
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
    return response


@staff_member_required(login_url='/admin/login/')
def toggle_admin_language(request):
    redirect_to = request.META.get('HTTP_REFERER', '/admin/')
    current = request.COOKIES.get(_ADMIN_LANG_COOKIE, 'uk')
    next_lang = 'en' if current == 'uk' else 'uk'
    response = redirect(redirect_to)
    response.set_cookie(
        _ADMIN_LANG_COOKIE,
        next_lang,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite='Lax',
    )
    return response


class HomeView(SEOMixin, TemplateView):
    template_name = 'core/home.html'
    seo_title = _('Masáž a relaxace Praha — Luxusní spa salon | Black Velvet')
    seo_description = _(
        'Black Velvet Spa — luxusní masážní salon v srdci Prahy. '
        'VIP a relaxační masáže, masáže pro ženy i pro páry. Rezervace přes WhatsApp.'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True)[:6]
        context['faqs'] = FAQ.objects.filter(is_active=True, page=FAQ.PAGE_HOME)
        context['reviews'] = Review.objects.filter(is_published=True)
        context['schema_website'] = True
        context['schema_faq'] = context['faqs'].exists()
        return context


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Disallow: /admin/',
        'Disallow: /api/',
        'Disallow: /rezervace/potvrdit/',
        'Disallow: /rezervace/krok/',
    ]
    for lang_code, _ in settings.LANGUAGES:
        if lang_code == settings.LANGUAGE_CODE:
            continue
        prefix = f'/{lang_code}'
        lines.append(f'Disallow: {prefix}/rezervace/potvrdit/')
        lines.append(f'Disallow: {prefix}/rezervace/krok/')
    lines += [
        '',
        f'Sitemap: {settings.SITE_URL.rstrip("/")}{reverse("sitemap")}',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def handler404(request, exception):
    return render(request, 'core/404.html', status=404)


def handler500(request):
    return render(request, 'core/500.html', status=500)
