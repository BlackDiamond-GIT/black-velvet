from html import unescape

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import translation

from django.conf import settings

from apps.core.models import SiteSettings
from apps.core.seed_loader import load_bundle
from apps.services.models import Service

from apps.core.i18n import translate_url_for_language


class DefaultLanguageRoutingTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_root_serves_czech_without_redirect(self):
        response = self.client.get(
            '/',
            HTTP_ACCEPT_LANGUAGE='en-US,en;q=0.9',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Language'], 'cs')

    def test_root_no_longer_redirects_to_en(self):
        response = self.client.get(
            '/',
            HTTP_ACCEPT_LANGUAGE='en-US,en;q=0.9',
        )
        self.assertNotEqual(response.status_code, 302)

    def test_english_still_available_under_prefix(self):
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Language'], 'en')

    def test_legacy_cs_prefix_redirects_to_root(self):
        response = self.client.get('/cs/')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], '/')

    def test_legacy_cs_path_redirects_without_prefix(self):
        response = self.client.get('/cs/masaze/')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], '/masaze/')

    def test_home_reverse_uses_unprefixed_czech_url(self):
        with translation.override('cs'):
            self.assertEqual(reverse('core:home'), '/')

    def test_translate_url_from_english_to_czech(self):
        self.assertEqual(translate_url_for_language('/en/', 'cs'), '/')
        self.assertEqual(translate_url_for_language('/en/masaze/', 'cs'), '/masaze/')

    def test_set_language_switches_from_english_to_czech(self):
        home_en = self.client.get('/en/')
        token = home_en.context['csrf_token']
        response = self.client.post(
            reverse('set_language'),
            {
                'language': 'cs',
                'next': '/en/',
                'csrfmiddlewaretoken': token,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(response['Content-Language'], 'cs')


class PragueRelaxPublicContentTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_defaults_use_new_salon_details(self):
        site = SiteSettings.load()
        self.assertEqual(settings.SITE_PHONE, '+420 776 739 466')
        self.assertEqual(settings.SITE_ADDRESS, 'Lužická 1416/29, 120 00 Vinohrady')
        self.assertEqual(site.get_active_phone_display(), '+420 776 739 466')
        self.assertEqual(site.get_active_whatsapp_number(), '420776739466')
        self.assertEqual(site.whatsapp_url, 'https://wa.me/420776739466')

    def test_home_uses_requested_seo_and_legal_notice(self):
        response = self.client.get('/')
        self.assertContains(response, 'Black Velvet Spa | Luxusní relaxační masáže Vinohrady')
        self.assertContains(response, 'Prémiový masážní salon v Praze na Vinohradech (Lužická 29).')
        self.assertContains(response, 'Prague relax s.r.o.')
        self.assertContains(response, 'IČO: 23481412')
        self.assertContains(response, 'registrovaná ochranná známka')

    def test_legal_notice_and_home_seo_are_translated(self):
        english = self.client.get('/en/')
        self.assertContains(english, 'The operator of Black Velvet Spa is Prague relax s.r.o.')
        self.assertContains(english, 'Black Velvet Spa | Luxury Relaxation Massages Vinohrady')
        self.assertIn(
            "Premium massage salon in Prague's Vinohrady district (Lužická 29).",
            unescape(english.content.decode()),
        )

        russian = self.client.get('/ru/')
        self.assertContains(russian, 'Оператор салона Black Velvet Spa')
        self.assertContains(russian, 'Black Velvet Spa | Роскошный расслабляющий массаж на Виноградах')
        self.assertContains(russian, 'Премиальный массажный салон в Праге на Виноградах (Lužická 29).')

    def test_contact_and_privacy_identify_operator_separately_from_salon(self):
        contact = self.client.get(reverse('pages:contact'))
        self.assertContains(contact, 'Provozovatel')
        self.assertContains(contact, 'Chvalská 718/10, Hloubětín, 198 00 Praha 9')
        self.assertContains(contact, 'Lužická 1416/29, 120 00 Vinohrady')

        privacy = self.client.get(reverse('pages:privacy'))
        self.assertContains(privacy, 'Správce údajů')
        self.assertContains(privacy, 'Provozovna')
        self.assertContains(privacy, 'Prague relax s.r.o.')

    def test_contact_places_operator_details_directly_under_address(self):
        for path in ('/kontakt/', '/en/kontakt/', '/ru/kontakt/'):
            response = self.client.get(path)
            html = response.content.decode()
            address_group = html.index('class="contact-card-group')
            address = html.index('Lužická 1416/29', address_group)
            operator = html.index('class="contact-operator"', address)
            company = html.index('Prague relax s.r.o.', operator)
            phone_card = html.index('tel:', company)
            self.assertLess(address, operator)
            self.assertLess(operator, company)
            self.assertLess(company, phone_card)

    def test_service_seed_has_requested_copy_and_no_active_elixir_seo(self):
        services = load_bundle()['services']
        by_slug = {service['slug']: service for service in services}
        self.assertEqual(
            by_slug['vip-masaz']['short_desc_cs'],
            'Exkluzivní a individuální celotělová péče s plnou pozorností certifikovaného terapeuta za využití prémiových bio olejů.',
        )
        self.assertEqual(
            by_slug['relaxacni-masaz']['short_desc_cs'],
            'Hluboká relaxační masáž celého těla s využitím prémiových bio olejů pro odbourání stresu a psychického napětí.',
        )
        self.assertEqual(
            by_slug['relaxacni-masaz']['short_desc_en'],
            'Deep full-body relaxation massage using premium organic oils to relieve stress and mental tension.',
        )
        self.assertEqual(
            by_slug['relaxacni-masaz']['short_desc_ru'],
            'Глубокий расслабляющий массаж всего тела с использованием премиальных био-масел для снятия стресса и психического напряжения.',
        )
        self.assertEqual(
            by_slug['masaz-pro-zeny']['short_desc_cs'],
            'Speciální masáž přizpůsobená potřebám ženského těla pro hlubokou relaxaci a harmonii.',
        )
        self.assertEqual(
            by_slug['masaz-pro-zeny']['short_desc_en'],
            'Special massage tailored to the needs of the female body for deep relaxation and harmony.',
        )
        self.assertEqual(
            by_slug['masaz-pro-zeny']['short_desc_ru'],
            'Специальный массаж, адаптированный к потребностям женского тела для глубокого расслабления и гармонии.',
        )
        active_short_copy = ' '.join(
            str(service.get(field, ''))
            for service in services
            if service.get('is_active')
            for field in ('short_desc_cs', 'short_desc_en', 'short_desc_ru')
        )
        self.assertNotIn('Zklidňující regenerační rituál', active_short_copy)
        self.assertNotIn('A soothing regenerative ritual', active_short_copy)
        self.assertNotIn('Успокаивающий восстанавливающий ритуал', active_short_copy)
        active_meta = ' '.join(
            service.get('meta_title', '')
            for service in services
            if service.get('is_active')
        )
        self.assertNotIn('Black Elixir', active_meta)


class PublicRoutingAndSeoTests(TestCase):
    LANGUAGE_PREFIXES = {
        'cs': '',
        'en': '/en',
        'ru': '/ru',
    }

    def test_price_label_is_localized_in_every_language(self):
        Service.objects.create(
            name='VIP masáž',
            name_cs='VIP masáž',
            name_en='VIP Massage',
            name_ru='VIP-массаж',
            slug='vip-masaz',
            short_desc='Test',
            short_desc_cs='Test',
            short_desc_en='Test',
            short_desc_ru='Тест',
            description='Test',
            description_cs='Test',
            description_en='Test',
            description_ru='Тест',
            duration_min=30,
            duration_max=90,
            price_czk=1800,
            price_label='od 1800 Kč',
            is_active=True,
        )
        expected = {
            'cs': 'od 1800 Kč',
            'en': 'from 1800 Kč',
            'ru': 'от 1800 Kč',
        }
        for language, prefix in self.LANGUAGE_PREFIXES.items():
            response = self.client.get(f'{prefix}/masaze/vip-masaz/')
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, f'<dd>{expected[language]}</dd>', html=True)
        self.assertNotContains(
            self.client.get('/en/masaze/vip-masaz/'),
            'Price from od',
        )
        self.assertNotContains(
            self.client.get('/ru/masaze/vip-masaz/'),
            'Цена от od',
        )

    def test_masseuse_detail_redirect_ignores_slug_in_every_language(self):
        for language, prefix in self.LANGUAGE_PREFIXES.items():
            response = self.client.get(f'{prefix}/maserky/julia/')
            self.assertRedirects(
                response,
                f'{prefix}/' if prefix else '/',
                fetch_redirect_response=False,
            )

    def test_retired_services_redirect_in_every_language(self):
        retired_slugs = (
            'aromaterapie',
            'cbd-relaxacni-masaz',
            'klasicka-masaz',
            'lymfaticka-masaz',
        )
        for language, prefix in self.LANGUAGE_PREFIXES.items():
            for retired_slug in retired_slugs:
                response = self.client.get(
                    f'{prefix}/masaze/{retired_slug}/'
                )
                self.assertRedirects(
                    response,
                    f'{prefix}/masaze/relaxacni-masaz/',
                    status_code=301,
                    fetch_redirect_response=False,
                )

    def test_robots_and_sitemap_cover_all_public_languages(self):
        robots = self.client.get('/robots.txt')
        self.assertEqual(robots.status_code, 200)
        self.assertContains(
            robots,
            'Sitemap: https://black-velvet.cz/sitemap.xml',
        )
        self.assertContains(robots, 'Disallow: /en/rezervace/krok/')
        self.assertContains(robots, 'Disallow: /ru/rezervace/krok/')

        sitemap = self.client.get('/sitemap.xml')
        self.assertEqual(sitemap.status_code, 200)
        self.assertIn('application/xml', sitemap['Content-Type'])
        sitemap_xml = sitemap.content.decode()
        self.assertIn('https://testserver/', sitemap_xml)
        self.assertIn('https://testserver/en/', sitemap_xml)
        self.assertIn('https://testserver/ru/', sitemap_xml)
        for language in ('cs', 'en', 'ru', 'x-default'):
            self.assertIn(f'hreflang="{language}"', sitemap_xml)
        for retired_slug in (
            'aromaterapie',
            'cbd-relaxacni-masaz',
            'klasicka-masaz',
            'lymfaticka-masaz',
        ):
            self.assertNotIn(retired_slug, sitemap_xml)
