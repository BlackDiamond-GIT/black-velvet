from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView

from apps.core.breadcrumbs import crumb, home_crumb
from apps.core.mixins import SEOMixin
from apps.media_library.cloudinary_urls import normalize_cloudinary_url
from apps.pages.models import FAQ

from .models import Service


LEGACY_SERVICE_REDIRECTS = {
    'aromaterapie': 'relaxacni-masaz',
    'cbd-relaxacni-masaz': 'relaxacni-masaz',
    'klasicka-masaz': 'relaxacni-masaz',
    'lymfaticka-masaz': 'relaxacni-masaz',
}


class ServiceListView(SEOMixin, ListView):
    model = Service
    template_name = 'services/list.html'
    context_object_name = 'services'
    seo_title = _('Relaxační masáže Praha | Black Velvet')
    seo_description = _(
        'Kompletní nabídka masáží v Praze — VIP masáž, relaxační masáž, '
        'masáž pro ženy a masáž pro páry. Rezervujte termín online.'
    )

    def get_queryset(self):
        return Service.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [home_crumb(), crumb(_('Masáže'))]
        context['schema_breadcrumb'] = True
        return context


class ServiceDetailView(SEOMixin, DetailView):
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        target_slug = LEGACY_SERVICE_REDIRECTS.get(kwargs.get('slug'))
        if target_slug:
            return redirect(
                'services:detail',
                slug=target_slug,
                permanent=True,
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Service.objects.filter(is_active=True)

    def get_seo_title(self):
        obj = self.object
        return obj.meta_title or f'{obj.name} Praha — Masáž a relaxace | Black Velvet'

    def get_seo_description(self):
        obj = self.object
        return obj.meta_description or obj.short_desc

    def get_seo_og_image(self):
        if self.object.image:
            url = normalize_cloudinary_url(self.object.image.url)
            return self.request.build_absolute_uri(url)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = FAQ.objects.filter(is_active=True, page=FAQ.PAGE_SERVICE)
        context['related_services'] = (
            Service.objects.filter(is_active=True).exclude(pk=self.object.pk)[:3]
        )
        context['breadcrumbs'] = [
            home_crumb(),
            crumb(_('Masáže'), 'services:list'),
            crumb(self.object.name),
        ]
        context['schema_service'] = True
        context['schema_faq'] = context['faqs'].exists()
        context['schema_breadcrumb'] = True
        return context
