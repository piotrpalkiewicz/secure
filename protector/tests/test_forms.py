import unittest
from unittest import mock

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from protector.forms import ResourceForm


class ResourceFormTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.form_class = ResourceForm

    def test_resource_form_should_be_invalid_when_empty(self):
        form = self.form_class()
        self.assertFalse(form.is_valid())

    def test_resource_form_should_be_invalid_when_url_and_file_are_set(self):
        data = {
            "url": "https://example.com",
        }
        files = {"file": mock.MagicMock(spec=File)}
        form = self.form_class(data=data, files=files)
        self.assertFalse(form.is_valid())

    def test_resource_form_should_be_valid_when_file_is_set(self):
        files = {
            "file": SimpleUploadedFile(
                "file.png", b"file_content", content_type="image/png"
            )
        }
        form = self.form_class(data={}, files=files)
        self.assertTrue(form.is_valid())

    def test_resource_form_should_be_valid_when_url_is_set(self):
        data = {"url": "https://example.com"}
        form = self.form_class(data=data)
        self.assertTrue(form.is_valid())
