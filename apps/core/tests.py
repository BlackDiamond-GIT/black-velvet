from django.test import Client, TestCase
from django.urls import reverse

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
