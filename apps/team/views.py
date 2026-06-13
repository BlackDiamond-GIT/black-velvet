from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView

from apps.core.breadcrumbs import crumb, home_crumb
from apps.core.mixins import SEOMixin

from .models import Masseuse


class TeamListView(SEOMixin, ListView):
    model = Masseuse
    template_name = 'team/list.html'
    context_object_name = 'masseuses'
    seo_title = _('Naše masérky Praha — Odbornice Black Velvet Spa')
    seo_description = _(
        'Seznamte se s našimi certifikovanými masérkami v Praze. '
        'Aromaterapie, sportovní a relaxační masáže od profesionálek.'
    )

    def get_queryset(self):
        return Masseuse.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [home_crumb(), crumb(_('Masérky'))]
        context['schema_breadcrumb'] = True
        return context


class MasseuseDetailView(SEOMixin, DetailView):
    model = Masseuse
    template_name = 'team/detail.html'
    context_object_name = 'masseuse'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Masseuse.objects.filter(is_active=True)

    def get_seo_title(self):
        obj = self.object
        return obj.meta_title or f'{obj.name} — Masérka Praha | Black Velvet'

    def get_seo_description(self):
        obj = self.object
        return obj.meta_description or obj.bio[:160]

    def get_seo_og_image(self):
        if self.object.photo:
            return self.request.build_absolute_uri(self.object.photo.url)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            home_crumb(),
            crumb(_('Masérky'), 'team:list'),
            crumb(self.object.name),
        ]
        context['schema_person'] = True
        context['schema_breadcrumb'] = True
        return context
