from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from apps.pages.models import FAQ, Review
from apps.services.models import Service
from apps.team.models import Masseuse

from .mixins import SEOMixin


class HomeView(SEOMixin, TemplateView):
    template_name = 'core/home.html'
    seo_title = _('Masáž a relaxace Praha — Luxusní spa salon | Black Velvet')
    seo_description = _(
        'Black Velvet Spa — luxusní masážní salon v srdci Prahy. '
        'Aromaterapeutické, relaxační a sportovní masáže. Rezervujte online.'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True)[:6]
        context['team'] = Masseuse.objects.filter(is_active=True)[:4]
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
    ]
    for lang_code, _ in settings.LANGUAGES:
        lines.append(f'Disallow: /{lang_code}/rezervace/potvrdit/')
        lines.append(f'Disallow: /{lang_code}/rezervace/wizard/')
    lines += [
        '',
        f'Sitemap: {settings.SITE_URL.rstrip("/")}{reverse("sitemap")}',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def handler404(request, exception):
    return render(request, 'core/404.html', status=404)


def handler500(request):
    return render(request, 'core/500.html', status=500)
