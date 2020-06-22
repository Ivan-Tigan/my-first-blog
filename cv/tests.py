from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from .views import cv, cv_edit

# Create your tests here.
class CVTest(TestCase):
    def test_cv_url_resolves_to_cv_view(self):
        found = resolve("/cv/")
        self.assertEqual(found.func, cv)
    def test_cv_returns_correct_template(self):
        response = self.client.get('/cv/')
        html = response.content.decode('utf8')

        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>CV</title>', html)
        self.assertTrue(html.endswith('</html>'))

        self.assertTemplateUsed(response, 'cv.html')
        
    def test_cv_edit_url_resolved_to_cv_edit_view(self):
        self.assertEqual(resolve("/cv/edit/").func, cv_edit)