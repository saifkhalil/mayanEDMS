from django.urls import re_path import url

from .views import DashboardDetailView, DashboardListView

urlpatterns = [
    re_path(
        regex=r'^dashboards/$', name='dashboard_list',
        view=DashboardListView.as_view()
    ),
    re_path(
        regex=r'^dashboards/(?P<dashboard_name>[-\w]+)/$',
        name='dashboard_detail', view=DashboardDetailView.as_view()
    )
]
