from django.utils.translation import gettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(
    label=_('Search'), name='search'
)

permission_search_tools = namespace.add_permission(
    label=_('Execute search tools'), name='search_tools'
)
