from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import MessageTestMixin


class MessageModelTestCase(MessageTestMixin, BaseTestCase):
    def test_method_get_absolute_re_path(self):
        self._create_test_message()

        self._clear_events()

        self.assertTrue(self._test_message.get_absolute_re_path())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
