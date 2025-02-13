from django.utils.translation import gettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_DOWNLOAD_FILE_EXPIRATION_INTERVAL,
    DEFAULT_SHARED_UPLOADED_FILE_EXPIRATION_INTERVAL,
    DEFAULT_STORAGE_DOWNLOAD_FILE_STORAGE,
    DEFAULT_STORAGE_DOWNLOAD_FILE_STORAGE_ARGUMENTS,
    DEFAULT_STORAGE_SHARED_STORAGE, DEFAULT_STORAGE_SHARED_STORAGE_ARGUMENTS,
    DEFAULT_STORAGE_TEMPORARY_DIRECTORY
)

namespace = SettingNamespace(
    label=_('Storage'), name='storage'
)

setting_download_file_expiration_interval = namespace.add_setting(
    default=DEFAULT_DOWNLOAD_FILE_EXPIRATION_INTERVAL,
    global_name='DOWNLOAD_FILE_EXPIRATION_INTERVAL', help_text=_(
        'Time in seconds, after which download files will be deleted.'
    )
)
setting_download_file_storage = namespace.add_setting(
    default=DEFAULT_STORAGE_DOWNLOAD_FILE_STORAGE,
    global_name='STORAGE_DOWNLOAD_FILE_STORAGE', help_text=_(
        'A storage backend that all workers can use to generate and hold '
        'files for download.'
    )
)
setting_download_file_storage_arguments = namespace.add_setting(
    default=DEFAULT_STORAGE_DOWNLOAD_FILE_STORAGE_ARGUMENTS,
    global_name='STORAGE_DOWNLOAD_FILE_STORAGE_ARGUMENTS',
)
setting_shared_storage = namespace.add_setting(
    default=DEFAULT_STORAGE_SHARED_STORAGE,
    global_name='STORAGE_SHARED_STORAGE', help_text=_(
        'A storage backend that all workers can use to share files.'
    )
)
setting_shared_storage_arguments = namespace.add_setting(
    default=DEFAULT_STORAGE_SHARED_STORAGE_ARGUMENTS,
    global_name='STORAGE_SHARED_STORAGE_ARGUMENTS'
)
setting_temporary_directory = namespace.add_setting(
    default=DEFAULT_STORAGE_TEMPORARY_DIRECTORY,
    global_name='STORAGE_TEMPORARY_DIRECTORY', help_text=_(
        'Temporary directory used site wide to store thumbnails, previews '
        'and temporary files.'
    )
)
setting_shared_uploaded_file_expiration_interval = namespace.add_setting(
    default=DEFAULT_SHARED_UPLOADED_FILE_EXPIRATION_INTERVAL,
    global_name='SHARED_UPLOADED_FILE_EXPIRATION_INTERVAL', help_text=_(
        'Time in seconds, after which temporary uploaded files will be '
        'deleted.'
    )
)
