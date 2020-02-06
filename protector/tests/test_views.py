from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory, tag
from django.urls import reverse

from protector.forms import ResourceForm
from protector.models import Resource
from protector.tests.factories import UserFactory
from protector.views import ResourceCreateView


@tag("integration")
class ResourceCreateViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()

    def test_view_get_status_code(self):
        request = self.factory.get(reverse("protector-resource_create"))
        request.user = self.user
        response = ResourceCreateView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_view_contains_form(self):
        request = self.factory.get(reverse("protector-resource_create"))
        request.user = self.user
        response = ResourceCreateView.as_view()(request)

        self.assertEqual(response.context_data["form"].__class__, ResourceForm)

    def test_view_post_should_create_resource_object(self):
        data = {"url": "https://example.com"}
        request = self.factory.post(reverse("protector-resource_create"), data=data)
        request.user = self.user
        ResourceCreateView.as_view()(request)

        self.assertTrue(Resource.objects.exists())

    def test_view_post_should_add_resource_author(self):
        data = {"url": "https://example.com"}
        request = self.factory.post(reverse("protector-resource_create"), data=data)
        request.user = self.user
        ResourceCreateView.as_view()(request)

        self.assertEqual(Resource.objects.first().author, self.user)

    def test_view_post_should_add_resource_hashed_url(self):
        data = {"url": "https://example.com"}
        request = self.factory.post(reverse("protector-resource_create"), data=data)
        request.user = self.user
        ResourceCreateView.as_view()(request)

        resource = Resource.objects.first()
        self.assertTrue(
            resource.protected_url,
            reverse("protector-resource_protected", args=(resource.pk,)),
        )

    def test_view_should_redirect_to_login_page_when_user_is_not_logged_in(self):
        request = self.factory.get(reverse("protector-resource_create"))
        request.user = AnonymousUser()
        response = ResourceCreateView.as_view()(request)

        self.assertEqual(response.status_code, 302)


@tag("integration")
class ResourceDetailViewTestCase(TestCase):
    pass
