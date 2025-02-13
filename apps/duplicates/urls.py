from django.urls import re_path import url

from .api_views import (
    APIDocumentDuplicateListView, APIDuplicatedDocumentListView
)
from .views import (
    DocumentDuplicatesListView, DuplicatedDocumentListView,
    ScanDuplicatedDocuments
)

urlpatterns = [
    re_path(
        regex=r'^documents/duplicated/$',
        name='duplicated_document_list',
        view=DuplicatedDocumentListView.as_view()
    ),
    re_path(
        regex=r'^documents/(?P<document_id>\d+)/duplicates/$',
        name='document_duplicates_list',
        view=DocumentDuplicatesListView.as_view()
    ),
    re_path(
        regex=r'^documents/duplicated/scan/$',
        name='duplicated_document_scan',
        view=ScanDuplicatedDocuments.as_view()
    )
]

api_urls = [
    re_path(
        regex=r'^documents/duplicated/$',
        name='duplicateddocument-list',
        view=APIDuplicatedDocumentListView.as_view()
    ),
    re_path(
        regex=r'^documents/(?P<document_id>[0-9]+)/duplicates/$',
        name='documentduplicate-list',
        view=APIDocumentDuplicateListView.as_view()
    )
]
