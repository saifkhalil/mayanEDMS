from django.urls import re_path import url

from .api_views import (
    APIDocumentTagAttachView, APIDocumentTagRemoveView,
    APIDocumentTagListView, APITagDocumentListView, APITagListView,
    APITagDetailView
)
from .views import (
    DocumentTagListView, TagAttachActionView, TagCreateView,
    TagDeleteView, TagEditView, TagListView, TagRemoveActionView,
    TagDocumentListView
)

urlpatterns_documents = [
    re_path(
        regex=r'^documents/(?P<document_id>\d+)/tags/$',
        name='document_tag_list', view=DocumentTagListView.as_view()
    ),
    re_path(
        regex=r'^documents/(?P<document_id>\d+)/tags/multiple/attach/$',
        name='tag_attach', view=TagAttachActionView.as_view()
    ),
    re_path(
        regex=r'^documents/(?P<document_id>\d+)/tags/multiple/remove/$',
        name='single_document_multiple_tag_remove',
        view=TagRemoveActionView.as_view()
    ),
    re_path(
        regex=r'^documents/multiple/tags/multiple/remove/$',
        name='multiple_documents_selection_tag_remove',
        view=TagRemoveActionView.as_view()
    ),
    re_path(
        regex=r'^documents/multiple/tags/multiple/attach/$',
        name='multiple_documents_tag_attach',
        view=TagAttachActionView.as_view()
    )
]

urlpatterns_tags = [
    re_path(regex=r'^tags/$', name='tag_list', view=TagListView.as_view()),
    re_path(
        regex=r'^tags/create/$', name='tag_create',
        view=TagCreateView.as_view()
    ),
    re_path(
        regex=r'^tags/(?P<tag_id>\d+)/delete/$', name='tag_single_delete',
        view=TagDeleteView.as_view()
    ),
    re_path(
        regex=r'^tags/(?P<tag_id>\d+)/edit/$', name='tag_edit',
        view=TagEditView.as_view()
    ),
    re_path(
        regex=r'^tags/(?P<tag_id>\d+)/documents/$', name='tag_document_list',
        view=TagDocumentListView.as_view()
    ),
    re_path(
        regex=r'^tags/multiple/delete/$', name='tag_multiple_delete',
        view=TagDeleteView.as_view()
    )
]

urlpatterns = []
urlpatterns.extend(urlpatterns_documents)
urlpatterns.extend(urlpatterns_tags)

api_urls = [
    re_path(regex=r'^tags/$', view=APITagListView.as_view(), name='tag-list'),
    re_path(
        regex=r'^tags/(?P<tag_id>[0-9]+)/$', view=APITagDetailView.as_view(),
        name='tag-detail'
    ),
    re_path(
        regex=r'^tags/(?P<tag_id>[0-9]+)/documents/$',
        view=APITagDocumentListView.as_view(), name='tag-document-list'
    ),
    re_path(
        regex=r'^documents/(?P<document_id>[0-9]+)/tags/$',
        view=APIDocumentTagListView.as_view(), name='document-tag-list'
    ),
    re_path(
        regex=r'^documents/(?P<document_id>[0-9]+)/tags/attach/$',
        name='document-tag-attach', view=APIDocumentTagAttachView.as_view()
    ),
    re_path(
        regex=r'^documents/(?P<document_id>[0-9]+)/tags/remove/$',
        name='document-tag-remove', view=APIDocumentTagRemoveView.as_view()
    )
]
