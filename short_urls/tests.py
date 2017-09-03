from django.test import TestCase
from .baseconvert import baseconvert, BASE10, BASE62
from django.core.urlresolvers import reverse
from django.test import Client
from .models import UrlPair


class BaseConversionTests(TestCase):

    def test_base_conversion_from_10_to_62(self):
        base_62 = baseconvert('12345', BASE10, BASE62)
        self.assertEqual('DNH', base_62)
        base_10 = baseconvert('DNH', BASE62, BASE10)
        self.assertEqual('12345', base_10)

class ViewTests(TestCase):

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_valid_params(self):
        response = self.client.get('/shorten/?long_url=www.eldiario.es')
        self.assertTemplateUsed(response, 'short_urls/shorten_result_ok.html')

    def test_invalid_params(self):
        response = self.client.get('/shorten/?long_url=nourl')
        self.assertTemplateUsed(response, 'short_urls/shorten_result_error.html')

    def test_redirection(self):
        expected_url = "http://www.eldiario.es"
        url_pair = UrlPair.create("C", expected_url)
        url_pair.save()

        response = self.client.get('/C')
        self.assertRedirects(response, expected_url, 
                status_code = 301)



