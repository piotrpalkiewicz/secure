from django.test import TestCase, RequestFactory
from django.urls import reverse

from protector.forms import ResourceForm
from protector.views import ResourceCreateView


class ResourceCreateViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_view_get_status_code(self):
        request = self.factory.get(reverse("resources-create"))
        response = ResourceCreateView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_view_contains_form(self):
        request = self.factory.get(reverse("resources-create"))
        response = ResourceCreateView.as_view()(request)

        self.assertEqual(response.context_data["form"].__class__, ResourceForm)
