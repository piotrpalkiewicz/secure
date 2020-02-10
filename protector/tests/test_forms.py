import unittest

from protector.forms import ResourcePermissionForm
from protector.tests.factories import ResourceFactory


class ResourcePermissionFormTestCase(unittest.TestCase):
    def setUp(self):
        self.resource = ResourceFactory()
        self.form_class = ResourcePermissionForm

    def test_form_should_be_valid_when_password_matches(self):
        password = self.resource.password

        form = self.form_class(
            {"password": password, "protected_url": self.resource.protected_url}
        )

        self.assertTrue(form.is_valid())

    def test_form_should_be_invalid_when_password_matches(self):
        password = "not_match"

        form = self.form_class(
            {"password": password, "protected_url": self.resource.protected_url}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)
