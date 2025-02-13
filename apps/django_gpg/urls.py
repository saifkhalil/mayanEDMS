from django.urls import re_path import url

from .api_views import APIKeyListView, APIKeyView
from .views import (
    KeyDeleteView, KeyDetailView, KeyDownloadView, KeyQueryView,
    KeyQueryResultView, KeyReceive, KeyUploadView, PrivateKeyListView,
    PublicKeyListView
)

urlpatterns = [
    re_path(
        regex=r'^keys/(?P<key_id>\d+)/$', name='key_detail',
        view=KeyDetailView.as_view()
    ),
    re_path(
        regex=r'^keys/(?P<key_id>\d+)/delete/$', name='key_delete',
        view=KeyDeleteView.as_view()
    ),
    re_path(
        regex=r'^keys/(?P<key_id>\d+)/download/$', name='key_download',
        view=KeyDownloadView.as_view()
    ),
    re_path(
        regex=r'^keys/private/$', name='key_private_list',
        view=PrivateKeyListView.as_view()
    ),
    re_path(
        regex=r'^keys/public/$', name='key_public_list',
        view=PublicKeyListView.as_view()
    ),
    re_path(
        regex=r'^keys/upload/$', name='key_upload',
        view=KeyUploadView.as_view()
    ),
    re_path(
        regex=r'^keys/query/$', name='key_query', view=KeyQueryView.as_view()
    ),
    re_path(
        regex=r'^keys/query/results/$', name='key_query_results',
        view=KeyQueryResultView.as_view()
    ),
    # Key ID for this view is not the key's DB ID by the embedded
    # alphanumeric ID.
    re_path(
        regex=r'^keys/receive/(?P<key_id>.+)/$', name='key_receive',
        view=KeyReceive.as_view()
    )
]

api_urls = [
    re_path(
        regex=r'^keys/(?P<key_id>[0-9]+)/$', name='key-detail',
        view=APIKeyView.as_view()
    ),
    re_path(regex=r'^keys/$', name='key-list', view=APIKeyListView.as_view())
]
