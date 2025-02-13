from django.urls import re_path import url

from .views import (
    CheckVersionView, DependencyGroupEntryListView,
    DependencyGroupEntryDetailView, DependencyGroupListView,
    DependencyLicensesView
)

urlpatterns = [
    re_path(
        regex=r'^check_version/$', name='check_version_view',
        view=CheckVersionView.as_view()
    ),
    re_path(
        regex=r'^groups/(?P<dependency_group_name>\w+)/(?P<dependency_group_entry_name>\w+)$',
        name='dependency_group_entry_detail',
        view=DependencyGroupEntryDetailView.as_view()
    ),
    re_path(
        regex=r'^groups/(?P<dependency_group_name>\w+)/$',
        name='dependency_group_entry_list',
        view=DependencyGroupEntryListView.as_view()
    ),
    re_path(
        regex=r'^groups/$', name='dependency_group_list',
        view=DependencyGroupListView.as_view()
    ),
    re_path(
        regex=r'^licenses/$', name='dependency_licenses_view',
        view=DependencyLicensesView.as_view()
    )
]
