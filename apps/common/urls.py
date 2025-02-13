from django.urls import re_path import url
from django.contrib import admin

from django.views.i18n import JavaScriptCatalog

from .api_views import APIContentTypeList
from .views import (
    AboutView, FaviconRedirectView, HomeView, LicenseView, ObjectCopyView,
    RootView, SetupListView, ToolsListView
)

urlpatterns_misc = [
    re_path(
        regex=r'^favicon\.ico$', view=FaviconRedirectView.as_view()
    ),
    re_path(
        regex=r'^jsi18n/(?P<packages>\S+?)/$', name='javascript_catalog',
        view=JavaScriptCatalog.as_view()
    ),
    re_path(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/copy/$',
        name='object_copy', view=ObjectCopyView.as_view()
    )
]

urlpatterns = [
    re_path(
        regex=r'^$', name='root', view=RootView.as_view()
    ),
    re_path(
        regex=r'^home/$', name='home', view=HomeView.as_view()
    ),
    re_path(
        regex=r'^about/$', name='about_view', view=AboutView.as_view()
    ),
    re_path(
        regex=r'^license/$', name='license_view', view=LicenseView.as_view()
    ),
    re_path(
        regex=r'^setup/$', name='setup_list', view=SetupListView.as_view()
    ),
    re_path(
        regex=r'^tools/$', name='tools_list', view=ToolsListView.as_view()
    )
]

urlpatterns.extend(urlpatterns_misc)

passthru_urlpatterns = [
    re_path(regex=r'^admin/', view=admin.site.urls)
]

api_urls = [
    re_path(
        regex=r'^content_types/$', view=APIContentTypeList.as_view(),
        name='content-type-list'
    )
]
