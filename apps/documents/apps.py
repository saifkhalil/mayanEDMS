from django.db.models.signals import post_migrate, post_save
from django.utils.translation import gettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.permissions import (
    permission_acl_edit, permission_acl_view
)
from mayan.apps.app_manager.apps import MayanAppConfig
from mayan.apps.common.classes import MissingItem, ModelCopy
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_main, menu_multi_item, menu_object,
    menu_return, menu_secondary, menu_setup
)
from mayan.apps.common.signals import signal_post_initial_setup
from mayan.apps.converter.classes import AppImageErrorImage
from mayan.apps.converter.links import link_transformation_list
from mayan.apps.converter.permissions import (
    permission_transformation_create, permission_transformation_delete,
    permission_transformation_edit, permission_transformation_view
)
from mayan.apps.dashboards.dashboards import dashboard_administrator
from mayan.apps.databases.classes import (
    ModelField, ModelFieldRelated, ModelProperty, ModelQueryFields
)
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.file_caching.links import link_cache_partition_purge
from mayan.apps.file_caching.permissions import (
    permission_cache_partition_purge
)
from mayan.apps.forms import column_widgets
from mayan.apps.logging.classes import ErrorLog, ErrorLogDomain
from mayan.apps.navigation.source_columns import SourceColumn
from mayan.apps.rest_api.fields import DynamicSerializerField
from mayan.apps.templating.classes import AJAXTemplate
from mayan.apps.user_management.dashboards import dashboard_user

from .classes import DocumentFileAction, DocumentVersionModification
from .column_widgets import ThumbnailWidget
from .dashboard_widgets import (
    DashboardWidgetDocumentFilePagesTotal, DashboardWidgetDocumentsInTrash,
    DashboardWidgetDocumentsNewThisMonth,
    DashboardWidgetDocumentsPagesNewThisMonth, DashboardWidgetDocumentsTotal,
    DashboardWidgetDocumentsTypesTotal, DashboardWidgetUserFavoriteDocuments,
    DashboardWidgetUserRecentlyAccessedDocuments,
    DashboardWidgetUserRecentlyCreatedDocuments
)

# Documents

from .events import (
    event_document_created, event_document_edited, event_document_trashed,
    event_document_viewed, event_trashed_document_deleted,
    event_trashed_document_restored
)

# Document files

from .events import (
    event_document_file_created, event_document_file_deleted,
    event_document_file_edited
)

# Document types

from .events import (
    event_document_type_changed, event_document_type_edited,
    event_document_type_quick_label_created,
    event_document_type_quick_label_deleted,
    event_document_type_quick_label_edited
)

# Document versions

from .events import (
    event_document_version_created, event_document_version_deleted,
    event_document_version_edited, event_document_version_page_created,
    event_document_version_page_deleted, event_document_version_page_edited,
)

# All

from .handlers import (
    handler_create_default_document_type,
    handler_create_document_file_page_image_cache,
    handler_create_document_version_page_image_cache,
    handler_document_event_on_save
)
from .links.document_file_links import (
    link_document_file_delete, link_document_file_edit,
    link_document_file_introspect_multiple,
    link_document_file_introspect_single, link_document_file_list,
    link_document_file_multiple_delete,
    link_document_file_multiple_transformations_clear,
    link_document_file_preview, link_document_file_print_form,
    link_document_file_properties, link_document_file_return_list,
    link_document_file_return_to_document,
    link_document_file_transformations_clear,
    link_document_file_transformations_clone
)
from .links.document_file_page_links import (
    link_document_file_page_list, link_document_file_page_navigation_first,
    link_document_file_page_navigation_last,
    link_document_file_page_navigation_next,
    link_document_file_page_navigation_previous,
    link_document_file_page_return_to_document,
    link_document_file_page_return_to_document_file,
    link_document_file_page_return_to_document_file_page_list,
    link_document_file_page_rotate_left, link_document_file_page_rotate_right,
    link_document_file_page_view, link_document_file_page_view_reset,
    link_document_file_page_zoom_in, link_document_file_page_zoom_out
)
from .links.document_links import (
    link_document_list, link_document_multiple_type_change,
    link_document_preview, link_document_properties,
	link_my_document_list,
    link_document_properties_edit, link_document_recently_accessed_list,
    link_document_recently_created_list, link_document_type_change
)
from .links.document_type_links import (
    link_document_type_create, link_document_type_delete,
    link_document_type_edit, link_document_type_filename_create,
    link_document_type_filename_delete, link_document_type_filename_edit,
    link_document_type_filename_generator, link_document_type_filename_list,
    link_document_type_list, link_document_type_retention_policies,
    link_document_type_setup
)
from .links.document_version_links import (
    link_document_version_active, link_document_version_create,
    link_document_version_edit, link_document_version_list,
    link_document_version_modification, link_document_version_multiple_delete,
    link_document_version_multiple_transformations_clear,
    link_document_version_preview, link_document_version_print_form,
    link_document_version_return_list,
    link_document_version_return_to_document,
    link_document_version_single_delete,
    link_document_version_transformations_clear,
    link_document_version_transformations_clone
)
from .links.document_version_page_links import (
    link_document_version_page_delete, link_document_version_page_list,
    link_document_version_page_list_remap,
    link_document_version_page_navigation_first,
    link_document_version_page_navigation_last,
    link_document_version_page_navigation_next,
    link_document_version_page_navigation_previous,
    link_document_version_page_return_to_document,
    link_document_version_page_return_to_document_version,
    link_document_version_page_return_to_document_version_page_list,
    link_document_version_page_rotate_left,
    link_document_version_page_rotate_right, link_document_version_page_view,
    link_document_version_page_view_reset, link_document_version_page_zoom_in,
    link_document_version_page_zoom_out
)
from .links.favorite_links import (
    link_document_favorites_add, link_document_favorites_add_multiple,
    link_document_favorites_list, link_document_favorites_remove,
    link_document_favorites_remove_multiple
)
from .links.miscellaneous_links import link_decorations_list
from .links.trashed_document_links import (
    link_document_delete, link_document_list_deleted,
    link_document_multiple_delete, link_document_multiple_restore,
    link_document_multiple_trash, link_document_restore, link_document_trash,
    link_trash_can_empty
)
from .literals import (
    ERROR_LOG_DOMAIN_NAME, IMAGE_ERROR_DOCUMENT_FILE_HAS_NO_PAGES,
    IMAGE_ERROR_DOCUMENT_FILE_PAGE_TRANSFORMATION_ERROR,
    IMAGE_ERROR_DOCUMENT_VERSION_ACTIVE_MISSING,
    IMAGE_ERROR_DOCUMENT_VERSION_HAS_NO_PAGES,
    IMAGE_ERROR_DOCUMENT_VERSION_PAGE_TRANSFORMATION_ERROR
)
from .menus import menu_documents
from .models.document_models import RecentlyCreatedDocument

# Documents

from .permissions import (
    permission_document_change_type, permission_document_create,
    permission_document_edit, permission_document_properties_edit,
    permission_document_tools, permission_document_trash,
    permission_document_view
)

# DocumentFile

from .permissions import (
    permission_document_file_delete, permission_document_file_edit,
    permission_document_file_new, permission_document_file_print,
    permission_document_file_tools, permission_document_file_view
)

# DocumentType

from .permissions import (
    permission_document_type_delete, permission_document_type_edit,
    permission_document_type_view
)

# DocumentVersion

from .permissions import (
    permission_document_version_create, permission_document_version_delete,
    permission_document_version_edit, permission_document_version_print,
    permission_document_version_view
)

# TrashedDocument

from .permissions import (
    permission_trashed_document_delete, permission_trashed_document_restore
)


class DocumentsApp(MayanAppConfig):
    app_namespace = 'documents'
    app_url = 'documents'
    has_rest_api = True
    has_static_media = True
    has_tests = True
    name = 'mayan.apps.documents'
    verbose_name = _(message='Documents')

    def ready_document_favorites(self):
        FavoriteDocument = self.get_model(model_name='FavoriteDocument')
        FavoriteDocumentProxy = self.get_model(
            model_name='FavoriteDocumentProxy'
        )

        ModelPermission.register_inheritance(
            model=FavoriteDocument, related='document'
        )

        SourceColumn(
            func=lambda context: context['object'].favorites.get(
                user=context['request'].user
            ).datetime_added, include_label=True, is_sortable=True,
            label=_(message='Date and time added'), name='datetime_added',
            sort_field='favorites__datetime_added',
            source=FavoriteDocumentProxy
        )

        dashboard_user.add_widget(
            order=3, widget=DashboardWidgetUserFavoriteDocuments
        )

    def ready_document_files(self):
        AppImageErrorImage(
            name=IMAGE_ERROR_DOCUMENT_FILE_PAGE_TRANSFORMATION_ERROR,
            template_name='documents/errors/document_file_page_transformation_error.html'
        )
        AppImageErrorImage(
            name=IMAGE_ERROR_DOCUMENT_FILE_HAS_NO_PAGES,
            template_name='documents/errors/document_file_has_no_pages.html'
        )

        DocumentFile = self.get_model(model_name='DocumentFile')
        DocumentFilePage = self.get_model(model_name='DocumentFilePage')

        error_log = ErrorLog(app_config=self)
        error_log.register_model(model=DocumentFile)
        error_log.register_model(model=DocumentFilePage)

        DocumentFileAction.load_modules()

        dashboard_administrator.add_widget(
            order=1, widget=DashboardWidgetDocumentFilePagesTotal
        )

        EventModelRegistry.register(model=DocumentFile)
        EventModelRegistry.register(model=DocumentFilePage)

        ModelEventType.register(
            model=DocumentFile, event_types=(
                event_document_file_edited,
            )
        )

        ModelField(
            model=DocumentFilePage, label=_(message='Document file'),
            name='document_file'
        )
        ModelField(
            model=DocumentFilePage, label=_(message='Page number'),
            name='page_number'
        )

        ModelProperty(
            description=_(message='Return the document instance.'),
            model=DocumentFilePage, label=_(message='Document'),
            name='document'
        )

        ModelPermission.register(
            model=DocumentFile, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_cache_partition_purge,
                permission_document_file_delete,
                permission_document_file_edit,
                permission_document_file_print,
                permission_document_file_tools,
                permission_document_file_view,
                permission_transformation_create,
                permission_transformation_delete,
                permission_transformation_edit,
                permission_transformation_view
            )
        )

        ModelPermission.register_inheritance(
            model=DocumentFile, related='document'
        )
        ModelPermission.register_inheritance(
            model=DocumentFile, related='document__document_type'
        )
        ModelPermission.register_inheritance(
            model=DocumentFilePage, related='document_file'
        )

        model_query_fields_document_file = ModelQueryFields(
            model=DocumentFile
        )
        model_query_fields_document_file.add_prefetch_related_field(
            field_name='file_pages'
        )
        model_query_fields_document_file.add_select_related_field(
            field_name='document'
        )

        model_query_fields_document_file_page = ModelQueryFields(
            model=DocumentFilePage
        )
        model_query_fields_document_file_page.add_select_related_field(
            field_name='document_file'
        )

        # DocumentFile

        SourceColumn(
            attribute='datetime_created', include_label=True,
            is_sortable=True, name='datetime_created',
            source=RecentlyCreatedDocument
        )
        SourceColumn(
            source=DocumentFile, attribute='filename', is_identifier=True,
            is_object_absolute_url=True
        )
        SourceColumn(
            html_extra_classes='text-center document-thumbnail-list',
            label=_(message='Thumbnail'), order=-99, source=DocumentFile,
            widget=ThumbnailWidget
        )
        SourceColumn(
            func=lambda context: context['object'].pages.count(),
            include_label=True, label=_(message='Pages'), order=-6,
            source=DocumentFile
        )
        SourceColumn(
            attribute='comment', is_sortable=True, order=-7,
            source=DocumentFile
        )
        SourceColumn(
            attribute='encoding', include_label=True, is_sortable=True,
            order=-8, source=DocumentFile
        )
        SourceColumn(
            attribute='mimetype', include_label=True, is_sortable=True,
            order=-9, source=DocumentFile
        )
        SourceColumn(
            attribute='get_size_display', include_label=True,
            is_sortable=True, sort_field='size', source=DocumentFile
        )

        # DocumentFilePage

        SourceColumn(
            attribute='get_label', is_identifier=True,
            is_object_absolute_url=True, source=DocumentFilePage,
        )
        SourceColumn(
            html_extra_classes='text-center document-thumbnail-list',
            label=_(message='Thumbnail'), order=-99, source=DocumentFilePage,
            widget=ThumbnailWidget
        )

        # DocumentFile

        menu_list_facet.bind_links(
            links=(
                link_document_file_page_list, link_document_file_properties,
                link_document_file_preview
            ), sources=(DocumentFile,)
        )
        menu_multi_item.bind_links(
            links=(
                link_document_file_multiple_delete,
                link_document_file_introspect_multiple,
                link_document_file_multiple_transformations_clear,
            ), sources=(DocumentFile,)
        )
        menu_object.bind_links(
            links=(
                link_cache_partition_purge,
                link_document_file_delete,
                link_document_file_edit,
                link_document_file_introspect_single,
                link_document_file_print_form,
                link_document_file_transformations_clear,
                link_document_file_transformations_clone
            ),
            sources=(DocumentFile,)
        )
        menu_return.bind_links(
            links=(
                link_document_file_return_list,
                link_document_file_return_to_document,
            ), sources=(DocumentFile,)
        )

        # DocumentFilePages

        menu_facet.add_unsorted_source(source=DocumentFilePage)
        menu_facet.bind_links(
            links=(
                link_document_file_page_rotate_left,
                link_document_file_page_rotate_right,
                link_document_file_page_zoom_in,
                link_document_file_page_zoom_out,
                link_document_file_page_view_reset
            ), sources=('documents:document_file_page_view',)
        )
        menu_facet.bind_links(
            links=(
                link_document_file_page_view,
                link_document_file_page_navigation_first,
                link_document_file_page_navigation_previous,
                link_document_file_page_navigation_next,
                link_document_file_page_navigation_last
            ), sources=(DocumentFilePage,)
        )
        menu_list_facet.bind_links(
            links=(link_decorations_list, link_transformation_list),
            sources=(DocumentFilePage,)
        )
        menu_return.bind_links(
            links=(
                link_document_file_page_return_to_document,
                link_document_file_page_return_to_document_file,
                link_document_file_page_return_to_document_file_page_list
            ),
            sources=(DocumentFilePage,)
        )

        post_migrate.connect(
            dispatch_uid='documents_handler_create_document_file_page_image_cache',
            receiver=handler_create_document_file_page_image_cache
        )

    def ready_document_recently_accessed(self):
        RecentlyAccessedDocument = self.get_model(
            model_name='RecentlyAccessedDocument'
        )
        RecentlyAccessedDocumentProxy = self.get_model(
            model_name='RecentlyAccessedDocumentProxy'
        )

        ModelPermission.register_inheritance(
            model=RecentlyAccessedDocument, related='document',
        )

        SourceColumn(
            func=lambda context: context['object'].recent.first().datetime_accessed,
            include_label=True,
            is_sortable=True,
            label=_(message='Access date and time'),
            name='datetime_accessed',
            sort_field='recent__datetime_accessed',
            source=RecentlyAccessedDocumentProxy
        )

        dashboard_user.add_widget(
            order=1, widget=DashboardWidgetUserRecentlyAccessedDocuments
        )

    def ready_document_recently_created(self):
        dashboard_user.add_widget(
            order=2, widget=DashboardWidgetUserRecentlyCreatedDocuments
        )

    def ready_document_trashed(self):
        TrashedDocument = self.get_model(model_name='TrashedDocument')

        EventModelRegistry.register(model=TrashedDocument)

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=TrashedDocument
        )
        SourceColumn(
            attribute='trashed_date_time', include_label=True, order=99,
            source=TrashedDocument
        )

        dashboard_administrator.add_widget(
            order=2, widget=DashboardWidgetDocumentsInTrash
        )

        menu_object.bind_links(
            links=(link_document_restore, link_document_delete),
            sources=(TrashedDocument,)
        )
        menu_multi_item.bind_links(
            links=(
                link_document_multiple_restore, link_document_multiple_delete
            ), sources=(TrashedDocument,)
        )
        menu_multi_item.add_proxy_exclusion(source=TrashedDocument)
        menu_secondary.bind_links(
            links=(link_trash_can_empty,),
            sources=(
                'documents:document_list_deleted',
                'documents:trash_can_empty'
            )
        )

    def ready_document_types(self):
        DocumentType = self.get_model(model_name='DocumentType')
        DocumentTypeFilename = self.get_model(
            model_name='DocumentTypeFilename'
        )

        dashboard_administrator.add_widget(
            order=3, widget=DashboardWidgetDocumentsTypesTotal
        )

        EventModelRegistry.register(model=DocumentType)
        EventModelRegistry.register(model=DocumentTypeFilename)

        MissingItem(
            label=_(message='Create a document type'),
            description=_(
                message='Every uploaded document must be assigned a document type, '
                'it is the basic way Mayan EDMS categorizes documents.'
            ), condition=lambda: not DocumentType.objects.exists(),
            view='documents:document_type_list'
        )

        ModelCopy(model=DocumentTypeFilename).add_fields(
            field_names=(
                'document_type', 'filename', 'enabled'
            )
        )
        ModelCopy(
            model=DocumentType, bind_link=True, register_permission=True
        ).add_fields(
            field_names=(
                'label', 'trash_time_period', 'trash_time_unit',
                'delete_time_period', 'delete_time_unit', 'filenames'
            )
        )

        ModelEventType.register(
            model=DocumentType, event_types=(
                event_document_created, event_document_type_edited,
                event_document_type_quick_label_created,
                event_trashed_document_deleted
            )
        )
        ModelEventType.register(
            model=DocumentTypeFilename, event_types=(
                event_document_type_quick_label_deleted,
                event_document_type_quick_label_edited
            )
        )

        ModelPermission.register(
            model=DocumentType, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_document_create, permission_document_type_delete,
                permission_document_type_edit, permission_document_type_view
            )
        )

        ModelPermission.register_inheritance(
            model=DocumentTypeFilename, related='document_type'
        )

        # DocumentType

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=DocumentType
        )

        # DocumentTypeFilename

        SourceColumn(
            attribute='filename', is_identifier=True, is_sortable=True,
            source=DocumentTypeFilename
        )
        SourceColumn(
            attribute='enabled', include_label=True, is_sortable=True,
            source=DocumentTypeFilename, widget=column_widgets.TwoStateWidget
        )

        # DocumentType

        menu_list_facet.bind_links(
            links=(
                link_document_type_filename_list,
                link_document_type_filename_generator,
                link_document_type_retention_policies
            ), sources=(DocumentType,)
        )
        menu_object.bind_links(
            links=(
                link_document_type_delete, link_document_type_edit
            ), sources=(DocumentType,)
        )
        menu_return.bind_links(
            links=(link_document_type_list,),
            sources=(
                DocumentType, 'documents:document_type_create',
                'documents:document_type_list'
            )
        )
        menu_secondary.bind_links(
            links=(link_document_type_create,),
            sources=(
                DocumentType, 'documents:document_type_create',
                'documents:document_type_list'
            )
        )

        # DocumentTypeFilename

        menu_object.bind_links(
            links=(
                link_document_type_filename_edit,
                link_document_type_filename_delete
            ), sources=(DocumentTypeFilename,)
        )
        menu_secondary.bind_links(
            links=(link_document_type_filename_create,),
            sources=(
                DocumentTypeFilename,
                'documents:document_type_filename_list',
                'documents:document_type_filename_create'
            )
        )

        menu_setup.bind_links(
            links=(link_document_type_setup,)
        )

        signal_post_initial_setup.connect(
            dispatch_uid='documents_handler_create_default_document_type',
            receiver=handler_create_default_document_type
        )

    def ready_document_versions(self):
        DocumentVersion = self.get_model(model_name='DocumentVersion')
        DocumentVersionPage = self.get_model(model_name='DocumentVersionPage')
        DocumentVersionPageSearchResult = self.get_model(
            model_name='DocumentVersionPageSearchResult'
        )

        AppImageErrorImage(
            name=IMAGE_ERROR_DOCUMENT_VERSION_ACTIVE_MISSING,
            template_name='documents/errors/no_valid_version.html'
        )
        AppImageErrorImage(
            name=IMAGE_ERROR_DOCUMENT_VERSION_HAS_NO_PAGES,
            template_name='documents/errors/no_version_pages.html'
        )
        AppImageErrorImage(
            name=IMAGE_ERROR_DOCUMENT_VERSION_PAGE_TRANSFORMATION_ERROR,
            template_name='documents/errors/document_version_page_transformation_error.html'
        )

        DocumentVersionModification.load_modules()

        EventModelRegistry.register(model=DocumentVersion)
        EventModelRegistry.register(model=DocumentVersionPage)

        error_log = ErrorLog(app_config=self)
        error_log.register_model(model=DocumentVersion)
        error_log.register_model(model=DocumentVersionPage)

        ModelCopy(
            model=DocumentVersion, bind_link=True, register_permission=True
        ).add_fields(
            field_names=(
                'document', 'timestamp', 'comment', 'version_pages'
            )
        )
        ModelCopy(
            model=DocumentVersionPage, bind_link=True,
            register_permission=True
        ).add_fields(
            field_names=(
                'document_version', 'page_number', 'content_type',
                'object_id'
            )
        )

        ModelEventType.register(
            model=DocumentVersion, event_types=(
                event_document_version_edited,
                event_document_version_page_created,
                event_document_version_page_deleted
            )
        )
        ModelEventType.register(
            model=DocumentVersionPage, event_types=(
                event_document_version_page_edited,
            )
        )

        ModelPermission.register(
            model=DocumentVersion, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_cache_partition_purge,
                permission_document_version_delete,
                permission_document_version_edit,
                permission_document_version_print,
                permission_document_version_view,
                permission_transformation_create,
                permission_transformation_delete,
                permission_transformation_edit,
                permission_transformation_view
            )
        )

        # DocumentVersion

        ModelPermission.register_inheritance(
            model=DocumentVersion, related='document'
        )
        ModelPermission.register_inheritance(
            model=DocumentVersion, related='document__document_type'
        )

        # DocumentVersionPage

        ModelPermission.register_inheritance(
            model=DocumentVersionPage, related='document_version'
        )

        model_query_fields_document_version = ModelQueryFields(
            model=DocumentVersion
        )
        model_query_fields_document_version.add_prefetch_related_field(
            field_name='version_pages'
        )
        model_query_fields_document_version.add_select_related_field(
            field_name='document'
        )

        # DocumentVersion

        SourceColumn(
            source=DocumentVersion, attribute='get_label',
            is_identifier=True, is_object_absolute_url=True
        )
        SourceColumn(
            html_extra_classes='text-center document-thumbnail-list',
            label=_(message='Thumbnail'), order=-99, source=DocumentVersion,
            widget=ThumbnailWidget
        )
        SourceColumn(
            func=lambda context: context['object'].pages.count(),
            include_label=True, label=_(message='Pages'), order=-8,
            source=DocumentVersion
        )
        SourceColumn(
            attribute='active', include_label=True, is_sortable=True,
            order=-9, source=DocumentVersion, widget=column_widgets.TwoStateWidget
        )
        SourceColumn(
            attribute='comment', include_label=True, is_sortable=True,
            order=-7, source=DocumentVersion
        )

        # DocumentVersionPage

        SourceColumn(
            attribute='get_label', is_identifier=True,
            is_object_absolute_url=True, source=DocumentVersionPage,
        )
        SourceColumn(
            html_extra_classes='text-center document-thumbnail-list',
            label=_(message='Thumbnail'), order=-99,
            source=DocumentVersionPage, widget=ThumbnailWidget
        )

        # DocumentVersion

        menu_list_facet.bind_links(
            links=(
                link_document_version_page_list,
                link_document_version_preview
            ),
            sources=(DocumentVersion,)
        )
        menu_multi_item.bind_links(
            links=(
                link_document_version_multiple_delete,
                link_document_version_multiple_transformations_clear,
            ), sources=(DocumentVersion,)
        )
        menu_object.bind_links(
            links=(
                link_document_version_active, link_cache_partition_purge,
                link_document_version_single_delete,
                link_document_version_edit,
                link_document_version_modification,
                link_document_version_page_list_remap,
                link_document_version_print_form,
                link_document_version_transformations_clear,
                link_document_version_transformations_clone
            ),
            sources=(DocumentVersion,)
        )
        menu_return.bind_links(
            links=(
                link_document_version_return_list,
                link_document_version_return_to_document,
            ), sources=(DocumentVersion,)
        )

        # DocumentVersionPage

        menu_facet.add_unsorted_source(source=DocumentVersionPage)
        menu_facet.bind_links(
            links=(
                link_document_version_page_rotate_left,
                link_document_version_page_rotate_right,
                link_document_version_page_zoom_in,
                link_document_version_page_zoom_out,
                link_document_version_page_view_reset
            ), sources=('documents:document_version_page_view',)
        )
        menu_facet.bind_links(
            links=(link_document_version_page_view,),
            sources=(DocumentVersionPage,)
        )
        menu_facet.bind_links(
            links=(
                link_document_version_page_navigation_first,
                link_document_version_page_navigation_previous,
                link_document_version_page_navigation_next,
                link_document_version_page_navigation_last
            ), sources=(DocumentVersionPage,)
        )
        menu_list_facet.bind_links(
            links=(
                link_decorations_list, link_transformation_list,
            ), sources=(DocumentVersionPage, DocumentVersionPageSearchResult)
        )
        menu_object.bind_links(
            links=(
                link_document_version_page_delete,
            ), sources=(DocumentVersionPage, DocumentVersionPageSearchResult)
        )
        menu_return.bind_links(
            links=(
                link_document_version_page_return_to_document,
                link_document_version_page_return_to_document_version,
                link_document_version_page_return_to_document_version_page_list
            ), sources=(DocumentVersionPage,)
        )

        post_migrate.connect(
            dispatch_uid='documents_handler_create_document_version_page_image_cache',
            receiver=handler_create_document_version_page_image_cache
        )

    def ready_documents(self):
        AJAXTemplate(
            name='invalid_document',
            template_name='documents/invalid_document.html'
        )

        Document = self.get_model(model_name='Document')

        DynamicSerializerField.add_serializer(
            klass=Document,
            serializer_class='mayan.apps.documents.serializers.document_serializers.DocumentSerializer'
        )

        dashboard_administrator.add_widget(
            order=4, widget=DashboardWidgetDocumentsNewThisMonth
        )
        dashboard_administrator.add_widget(
            order=5, widget=DashboardWidgetDocumentsPagesNewThisMonth
        )
        dashboard_administrator.add_widget(
            order=0, widget=DashboardWidgetDocumentsTotal
        )

        EventModelRegistry.register(model=Document)

        error_log = ErrorLog(app_config=self)

        error_log.register_model(model=Document)

        ModelEventType.register(
            model=Document, event_types=(
                event_document_edited, event_document_type_changed,
                event_document_file_created, event_document_file_edited,
                event_document_file_deleted, event_document_version_created,
                event_document_version_edited,
                event_document_version_deleted, event_document_viewed,
                event_document_trashed, event_trashed_document_restored
            )
        )
        ModelField(model=Document, name='description')
        ModelField(model=Document, name='datetime_created')
        ModelField(model=Document, name='trashed_date_time')
        ModelField(
            model=Document, name='document_type'
        )
        ModelField(model=Document, name='in_trash')
        ModelField(model=Document, name='is_stub')
        ModelField(model=Document, name='label')
        ModelField(model=Document, name='language')
        ModelField(model=Document, name='uuid')
        ModelFieldRelated(model=Document, name='document_type__label')
        ModelFieldRelated(
            model=Document,
            name='files__checksum'
        )
        ModelFieldRelated(
            model=Document, label=_(message='File comments'),
            name='files__comment'
        )
        ModelFieldRelated(
            model=Document, label=_(message='File encodings'),
            name='files__encoding'
        )
        ModelFieldRelated(
            model=Document, label=_(message='File MIME types'),
            name='files__mimetype'
        )
        ModelFieldRelated(
            model=Document, label=_(message='File timestamps'),
            name='files__timestamp'
        )
        ModelProperty(
            description=_(message='Return the latest file of the document.'),
            model=Document, label=_(message='Latest file'),
            name='file_latest'
        )
        ModelProperty(
            description=_(message='Return the active version of the document.'),
            model=Document, label=_(message='Active version'),
            name='version_active'
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_document_change_type, permission_document_edit,
                permission_document_file_new,
                permission_document_properties_edit,
                permission_document_tools, permission_document_trash,
                permission_document_view, permission_document_version_create,
                permission_trashed_document_delete,
                permission_trashed_document_restore
            )
        )

        ModelPermission.register_inheritance(
            model=Document, related='document_type'
        )

        model_query_fields_document = ModelQueryFields(model=Document)
        model_query_fields_document.add_prefetch_related_field(
            field_name='files'
        )
        model_query_fields_document.add_prefetch_related_field(
            field_name='files__file_pages'
        )
        model_query_fields_document.add_select_related_field(
            field_name='document_type'
        )
        SourceColumn(
            func=lambda context: context['object'].from_cabinet,
            label=_(message='From'), include_label=True, order=-10, source=Document
        )
        SourceColumn(
            attribute='datetime_created', include_label=True,
            is_sortable=True, name='datetime_created', source=Document
        )
        SourceColumn(
            attribute='get_label', is_object_absolute_url=True,
            is_identifier=True, is_sortable=True, name='label',
            sort_field='label', source=Document
        )
        SourceColumn(
            html_extra_classes='text-center document-thumbnail-list',
            label=_(message='Thumbnail'), order=-99, source=Document,
            widget=ThumbnailWidget
        )
        SourceColumn(
            attribute='document_type', include_label=True, is_sortable=True,
            label=_(message='Type'), name='document_type', order=-9,
            source=Document
        )
        SourceColumn(
            func=lambda context: context['object'].pages.count(),
            label=_(message='Pages'), include_label=True, order=-8,
            source=Document
        )

        menu_list_facet.bind_links(
            links=(link_document_preview,), sources=(Document,), position=0
        )
        menu_list_facet.bind_links(
            links=(link_document_properties,), sources=(Document,),
            position=2
        )
        menu_list_facet.bind_links(
            links=(
                link_document_file_list, link_document_version_list
            ), sources=(Document,), position=2
        )
        menu_multi_item.bind_links(
            links=(
                link_document_favorites_add_multiple,
                link_document_favorites_remove_multiple,
                link_document_multiple_trash,
                link_document_multiple_type_change
            ), sources=(Document,)
        )
        menu_object.bind_links(
            links=(
                link_document_favorites_add, link_document_favorites_remove,
                link_document_properties_edit, link_document_type_change,
                link_document_trash
            ), sources=(Document,)
        )
        menu_secondary.bind_links(
            links=(link_document_version_create,),
            sources=(
                'documents:document_version_create',
                'documents:document_version_list'
            )
        )

        post_save.connect(
            dispatch_uid='documents_handler_document_event_on_save',
            receiver=handler_document_event_on_save, sender=Document
        )

    def ready(self):
        super().ready()

        self.ready_document_types()
        self.ready_documents()
        self.ready_document_trashed()
        self.ready_document_files()
        self.ready_document_versions()
        self.ready_document_favorites()
        self.ready_document_recently_accessed()
        self.ready_document_recently_created()

        ErrorLogDomain(
            label=_(message='Documents'), name=ERROR_LOG_DOMAIN_NAME
        )

        menu_documents.bind_links(
            links=(
                link_document_recently_accessed_list,
                link_document_recently_created_list,
                link_document_favorites_list, link_document_list,link_my_document_list,
                link_document_list_deleted
            )
        )

        menu_main.bind_links(
            links=(menu_documents,), position=10
        )
