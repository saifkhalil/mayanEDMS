from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import QuotaTestMixin


class QuotaModelTestCase(QuotaTestMixin, BaseTestCase):
    def test_method_get_absolute_re_path(self):
        self._create_test_quota()

        self._clear_events()

        self.assertTrue(self._test_quota.get_absolute_re_path())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
