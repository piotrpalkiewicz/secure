from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import TestCase, RequestFactory, tag
from django.urls import reverse
from django.utils import timezone

from protector import utils
from protector.forms import ResourceForm, ResourcePermissionForm
from protector.models import Resource
from protector.tests.factories import UserFactory, ResourceFactory
from protector.views import (
    ResourceCreateView,
    ResourceDetailView,
    ResourceProtectedDetailView,
)


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
            reverse("protector-protected_resource", args=(resource.pk,)),
        )

    def test_view_post_should_add_resource_password(self):
        data = {"url": "https://example.com"}
        request = self.factory.post(reverse("protector-resource_create"), data=data)
        request.user = self.user

        ResourceCreateView.as_view()(request)

        resource = Resource.objects.first()
        self.assertIsNotNone(resource.password)

    def test_view_should_redirect_to_login_page_when_user_is_not_logged_in(self):
        request = self.factory.get(reverse("protector-resource_create"))
        request.user = AnonymousUser()

        response = ResourceCreateView.as_view()(request)

        self.assertEqual(response.status_code, 302)


class ResourceDetailViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.resource = ResourceFactory(author=self.user)

    def test_view_get_status_code(self):
        request = self.factory.get(
            reverse("protector-resource_detail", args=(self.resource.pk,))
        )
        request.user = self.user

        response = ResourceDetailView.as_view()(request, pk=self.resource.pk)

        self.assertEqual(response.status_code, 200)

    def test_view_should_redirect_to_login_page_when_user_is_not_logged_in(self):
        request = self.factory.get(
            reverse("protector-resource_detail", args=(self.resource.pk,))
        )
        request.user = AnonymousUser()

        with self.assertRaises(PermissionDenied):
            ResourceDetailView.as_view()(request, pk=self.resource.pk)

    def test_view_should_return_403_when_user_is_not_an_resource_author(self):
        resource = ResourceFactory(author=UserFactory())
        request = self.factory.get(
            reverse("protector-resource_detail", args=(resource.pk,))
        )
        request.user = self.user

        with self.assertRaises(PermissionDenied):
            ResourceDetailView.as_view()(request, pk=resource.pk)

    def test_view_should_display_url_and_password(self):
        request = self.factory.get(
            reverse("protector-resource_detail", args=(self.resource.pk,))
        )
        request.user = self.user

        response = ResourceDetailView.as_view()(request, pk=self.resource.pk)

        self.assertContains(response, self.resource.protected_url)
        self.assertContains(response, self.resource.password)


class ResourceProtectedDetailViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.resource = ResourceFactory()

    def _get_requests_post_response(self, data):
        request = self.factory.post(
            reverse(
                "protector-protected_resource", args=(self.resource.protected_url,),
            ),
            data=data,
        )
        request.user = AnonymousUser()

        response = ResourceProtectedDetailView.as_view()(
            request, protected_url=self.resource.protected_url
        )
        return response

    def test_view_contains_form(self):
        request = self.factory.get(
            reverse("protector-protected_resource", args=(self.resource.protected_url,))
        )
        request.user = AnonymousUser()

        response = ResourceProtectedDetailView.as_view()(
            request, protected_url=self.resource.protected_url
        )

        self.assertEqual(
            response.context_data["form"].__class__, ResourcePermissionForm
        )

    def test_password_not_match_should_raise_validation_error(self):
        data = {"password": "not_match"}
        response = self._get_requests_post_response(data)

        self.assertFalse(response.context_data["form"].is_valid())

    def test_password_match_should_redirect_to_url(self):
        data = {"password": self.resource.password}
        response = self._get_requests_post_response(data)

        self.assertEqual(response.url, self.resource.url)

    def test_password_match_should_increment_visits(self):
        data = {"password": self.resource.password}
        self.assertEqual(self.resource.visits, 0)
        self._get_requests_post_response(data)

        self.resource.refresh_from_db()
        self.assertEqual(self.resource.visits, 1)

    def test_should_raise_404_when_link_out_of_date(self):
        three_days_ago = timezone.now() - timedelta(days=3)
        self.resource.created_at = three_days_ago
        self.resource.save()
        request = self.factory.get(
            reverse("protector-protected_resource", args=(self.resource.protected_url,))
        )
        request.user = AnonymousUser()

        with self.assertRaises(Http404):
            ResourceProtectedDetailView.as_view()(
                request, protected_url=self.resource.protected_url
            )
