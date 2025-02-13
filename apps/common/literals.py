from django.conf import settings

from django.utils.translation import gettext_lazy as _

import mayan

COMMAND_NAME_COMMON_INITIAL_SETUP = 'common_initial_setup'
COMMAND_NAME_COMMON_PERFORM_UPGRADE = 'common_perform_upgrade'
COMMAND_NAME_MIGRATE = 'migrate'

DEFAULT_COMMON_COLLAPSE_LIST_MENU_LIST_FACET = True
DEFAULT_COMMON_COLLAPSE_LIST_MENU_OBJECT = True
DEFAULT_COMMON_DISABLE_LOCAL_STORAGE = False
DEFAULT_COMMON_DISABLED_APPS = settings.COMMON_DISABLED_APPS
DEFAULT_COMMON_EXTRA_APPS = settings.COMMON_EXTRA_APPS
DEFAULT_COMMON_EXTRA_APPS_PRE = settings.COMMON_EXTRA_APPS_PRE
DEFAULT_COMMON_HOME_VIEW = 'common:home'
DEFAULT_COMMON_HOME_VIEW_DASHBOARD_NAME = 'user'
DEFAULT_COMMON_PROJECT_TITLE = mayan.__title__
DEFAULT_COMMON_PROJECT_URL = mayan.__website__
DEFAULT_TX_PATH = '/usr/local/bin/tx'

DEFAULT_TX_PATH = '/usr/local/bin/tx'

EMPTY_LABEL = '---------'

DJANGO_SQLITE_BACKEND = 'django.db.backends.sqlite3'

MESSAGE_DEPRECATION_WARNING = _(
    'This feature has been deprecated and will be removed in a future '
    'version.'
)

TIME_DELTA_UNIT_DAYS = 'days'
TIME_DELTA_UNIT_HOURS = 'hours'
TIME_DELTA_UNIT_MINUTES = 'minutes'

TIME_DELTA_UNIT_CHOICES = (
    (TIME_DELTA_UNIT_DAYS, _('Days')),
    (TIME_DELTA_UNIT_HOURS, _('Hours')),
    (TIME_DELTA_UNIT_MINUTES, _('Minutes'))
)
