import unittest

from datetime import date, timedelta
from unittest import mock

from protector.models import Resource
from protector.services import is_password_match, is_valid_link


class ServicesUnitTestCase(unittest.TestCase):

    @mock.patch.object(Resource, "objects")
    def test_is_password_match_should_return_true_when_password_match(self, resource_mock):
        resource_mock.get.return_value = mock.Mock()

        self.assertTrue(is_password_match(protected_url="", password=""))

    @mock.patch.object(Resource, "objects")
    def test_is_password_match_should_return_false_when_obj_not_found(self, resource_mock):
        resource_mock.get.side_effect = mock.Mock(side_effect=Resource.DoesNotExist)

        self.assertFalse(is_password_match(protected_url="", password=""))

    def test_is_valid_link_should_return_true_when_created_at_is_now(self):
        created_at = date.today()

        self.assertTrue(is_valid_link(created_at))

    def test_is_valid_link_should_return_false_when_created_at_was_three_days_ago(self):
        created_at = date.today() - timedelta(days=3)

        self.assertFalse(is_valid_link(created_at))
