from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, TemplateView
from django.views.generic.base import RedirectView

from apps.core.breadcrumbs import crumb, home_crumb
from apps.core.mixins import SEOMixin

from .forms import ContactForm
from .models import FAQ, PriceCategory
from .prices_data import build_price_list


class PricesView(SEOMixin, TemplateView):
    template_name = 'pages/prices.html'
    seo_title = _('Ceník masáží Praha — Ceny a délky | Black Velvet')
    seo_description = _(
        'Kompletní ceník masáží v Black Velvet Spa Praha. '
        'Transparentní ceny VIP masáže, relaxační masáže, masáže pro ženy a masáže pro páry.'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = PriceCategory.objects.prefetch_related('items').all()
        context['categories'] = categories
        context['price_items'] = build_price_list(categories)
        context['breadcrumbs'] = [home_crumb(), crumb(_('Ceník'))]
        context['schema_breadcrumb'] = True
        context['schema_prices'] = True
        return context


class ContactView(SEOMixin, FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    seo_title = _('Kontakt — Black Velvet Spa Vinohrady, Praha 2')
    seo_description = _(
        'Kontaktujte Black Velvet Spa ve Vinohradech, Praha 2. Adresa Lužická 1416/29, '
        'telefon, email a kontaktní formulář. Rezervace masáže online nebo telefonicky.'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = FAQ.objects.filter(is_active=True, page=FAQ.PAGE_GENERAL)[:4]
        context['breadcrumbs'] = [home_crumb(), crumb(_('Kontakt'))]
        context['schema_breadcrumb'] = True
        context['schema_contact'] = True
        return context

    def form_valid(self, form):
        message_obj = form.save()
        from django.conf import settings as django_settings

        send_mail(
            subject=f'Kontakt: {message_obj.name}',
            message=message_obj.message,
            from_email=message_obj.email,
            recipient_list=[django_settings.SITE_EMAIL],
            fail_silently=True,
        )
        if self.request.htmx:
            return render(self.request, 'pages/partials/contact_success.html')
        messages.success(self.request, _('Zpráva byla odeslána. Brzy se vám ozveme.'))
        return redirect('pages:contact')

    def form_invalid(self, form):
        if self.request.htmx:
            return render(
                self.request,
                'pages/partials/contact_form.html',
                {'form': form},
                status=422,
            )
        return super().form_invalid(form)


class ScheduleView(RedirectView):
    permanent = False
    pattern_name = 'core:home'


class AboutView(SEOMixin, TemplateView):
    template_name = 'pages/about.html'
    seo_title = _('O nás — Luxusní masážní salon Praha | Black Velvet')
    seo_description = _(
        'Black Velvet Spa — luxusní masážní salon v srdci Prahy 1. '
        'Profesionální masérky, klidné prostředí a individuální péče.'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [home_crumb(), crumb(_('O nás'))]
        context['schema_breadcrumb'] = True
        return context


class SalonRulesView(SEOMixin, TemplateView):
    template_name = 'pages/salon_rules.html'
    seo_title = _('Pravidla salonu | Black Velvet Spa Praha')
    seo_description = _(
        'Pravidla a zásady návštěvy Black Velvet Spa. '
        'Rezervace, zrušení termínu, hygiena a chování v salonu.'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [home_crumb(), crumb(_('Pravidla salonu'))]
        context['schema_breadcrumb'] = True
        return context


class PrivacyView(SEOMixin, TemplateView):
    template_name = 'pages/privacy.html'
    seo_title = _('Zásady ochrany osobních údajů | Black Velvet')
    seo_description = _(
        'Zásady ochrany osobních údajů Black Velvet Spa. '
        'Informace o zpracování dat a vašich právech.'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [home_crumb(), crumb(_('Zásady ochrany'))]
        context['schema_breadcrumb'] = True
        return context
