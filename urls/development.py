from django.conf import settings
from django.urls import re_path import include, url

from .base import *  # NOQA

if 'rosetta' in settings.INSTALLED_APPS:
    try:
        import rosetta  # NOQA
    except ImportError:
        pass
    else:
        urlpatterns += [  # NOQA
            re_path(
                regex=r'^rosetta/', view=include('rosetta.urls'),
                name='rosetta'
            )
        ]

if 'debug_toolbar' in settings.INSTALLED_APPS:
    try:
        import debug_toolbar
    except ImportError:
        pass
    else:
        urlpatterns += [  # NOQA
            re_path(
                regex=r'^__debug__/', view=include(debug_toolbar.urls)
            )
        ]

if 'silk' in settings.INSTALLED_APPS:
    try:
        import silk
    except ImportError:
        pass
    else:
        urlpatterns += [  # NOQA
            re_path(
                regex=r'^silk/', view=include('silk.urls', namespace='silk')
            )
        ]
