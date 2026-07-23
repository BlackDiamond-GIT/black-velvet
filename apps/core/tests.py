from django.test import Client, TestCase
from django.urls import reverse

from django.conf import settings

from apps.core.models import SiteSettings
from apps.core.seed_loader import load_bundle

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
        self.assertContains(response, 'Black Velvet Spa | Luxusní relaxační masáže Praha')
        self.assertContains(response, 'Prémiový masážní salon na Vinohradech na adrese Lužická 1416/29.')
        self.assertContains(response, 'Prague relax s.r.o.')
        self.assertContains(response, 'IČO: 23481412')
        self.assertContains(response, 'registrovaná ochranná známka')

    def test_legal_notice_and_home_seo_are_translated(self):
        english = self.client.get('/en/')
        self.assertContains(english, 'The operator of Black Velvet Spa is Prague relax s.r.o.')
        self.assertContains(english, 'Black Velvet Spa | Luxury Relaxation Massages Prague')

        russian = self.client.get('/ru/')
        self.assertContains(russian, 'Оператор салона Black Velvet Spa')
        self.assertContains(russian, 'Black Velvet Spa | Роскошный расслабляющий массаж в Праге')

    def test_contact_and_privacy_identify_operator_separately_from_salon(self):
        contact = self.client.get(reverse('pages:contact'))
        self.assertContains(contact, 'Provozovatel')
        self.assertContains(contact, 'Chvalská 718/10, Hloubětín, 198 00 Praha 9')
        self.assertContains(contact, 'Lužická 1416/29, 120 00 Vinohrady')

        privacy = self.client.get(reverse('pages:privacy'))
        self.assertContains(privacy, 'Správce údajů')
        self.assertContains(privacy, 'Provozovna')
        self.assertContains(privacy, 'Prague relax s.r.o.')

    def test_service_seed_has_requested_copy_and_no_active_elixir_seo(self):
        services = load_bundle()['services']
        by_slug = {service['slug']: service for service in services}
        self.assertEqual(
            by_slug['vip-masaz']['short_desc_cs'],
            'Exkluzivní a individuální celotělová péče s plnou pozorností certifikovaného terapeuta za využití prémiových bio olejů.',
        )
        self.assertEqual(
            by_slug['masaz-pro-zeny']['short_desc_cs'],
            'Zklidňující regenerační rituál v harmonickém a plně soukromém prostředí, zaměřený na odbourání stresu a hluboké uvolnění svalů.',
        )
        active_meta = ' '.join(
            service.get('meta_title', '')
            for service in services
            if service.get('is_active')
        )
        self.assertNotIn('Black Elixir', active_meta)
