import unittest
from unittest import mock

from django.core.exceptions import ValidationError
from django.core.files import File

from protector.models import Resource
from protector.tests.factories import ResourceFactory


class ResourceModelTestCase(unittest.TestCase):
    def test_resource_should_be_invalid_when_empty(self):
        resource = Resource()
        with self.assertRaises(ValidationError):
            resource.clean()

    def test_resource_form_should_be_invalid_when_url_and_file_are_set(self):
        file = mock.MagicMock(spec=File)
        file.name = "test.png"
        resource = Resource(url="https://example.com", file=file)
        with self.assertRaises(ValidationError):
            resource.clean()

    def test_resource_should_be_valid_when_file_is_set(self):
        file = mock.MagicMock(spec=File)
        file.name = "test.png"
        resource = Resource(file=file)

        resource.clean()

        self.assertEqual(resource.file, file)

    def test_resource_should_be_valid_when_url_is_set(self):
        url = "https://example.com"
        resource = Resource(url=url)

        resource.clean()

        self.assertEqual(resource.url, url)

    def test_resource_should_have_generated_url_and_password_after_save(self):
        resource = ResourceFactory()

        self.assertIsNotNone(resource.protected_url)
        self.assertIsNotNone(resource.password)
