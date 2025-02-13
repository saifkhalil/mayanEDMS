from django.urls import re_path import url

from .views import QueueListView

urlpatterns = [
    re_path(
        regex=r'^queues/$', view=QueueListView.as_view(),
        name='queue_list'
    )
]
