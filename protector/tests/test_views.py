from django.test import TestCase, RequestFactory, tag
from django.urls import reverse

from protector.forms import ResourceForm
from protector.models import Resource
from protector.views import ResourceCreateView


@tag("integration")
class ResourceCreateViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_view_get_status_code(self):
        request = self.factory.get(reverse("protector-resource_create"))
        response = ResourceCreateView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_view_contains_form(self):
        request = self.factory.get(reverse("protector-resource_create"))
        response = ResourceCreateView.as_view()(request)

        self.assertEqual(response.context_data["form"].__class__, ResourceForm)

    def test_view_post_should_create_resource_object(self):
        data = {"url": "https://example.com"}
        request = self.factory.post(reverse("protector-resource_create"), data=data)
        response = ResourceCreateView.as_view()(request)

        self.assertTrue(Resource.objects.exists())
