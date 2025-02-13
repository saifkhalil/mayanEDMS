from django.urls import re_path import url

from .views import (
    StatisticNamespaceDetailView, StatisticNamespaceListView,
    StatisticTypeDetailView, StatisticTypeQueueView
)

urlpatterns = [
    re_path(
        regex=r'^namespaces/$', view=StatisticNamespaceListView.as_view(),
        name='statistic_namespace_list'
    ),
    re_path(
        regex=r'^namespaces/(?P<slug>[\w-]+)/$',
        view=StatisticNamespaceDetailView.as_view(),
        name='statistic_namespace_detail'
    ),
    re_path(
        regex=r'^namespaces/statistics/(?P<slug>[\w-]+)/view/$',
        view=StatisticTypeDetailView.as_view(), name='statistic_detail'
    ),
    re_path(
        regex=r'^namespaces/statistics/(?P<slug>[\w-]+)/queue/$',
        view=StatisticTypeQueueView.as_view(), name='statistic_queue'
    )
]
