from mayan.apps.testing.tests.base import BaseTestCase


class GroupEventsViewTestCase(BaseTestCase):
    def test_user_method_get_absolute_re_path(self):
        self._create_test_user()

        self._test_user.get_absolute_re_path()
