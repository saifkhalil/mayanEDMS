from django.utils.translation import gettext_lazy as _

from ..icons import icon_document_recently_created_list
from ..models.document_models import RecentlyCreatedDocument

from .document_views import DocumentListView
from mayan.apps.cabinets.models import Cabinet

class RecentCreatedDocumentListView(DocumentListView):
    view_icon = icon_document_recently_created_list

    def get_document_queryset(self):
        if self.request.user.is_superuser:
           return RecentlyCreatedDocument.valid.all()
        else:
           cabinets = Cabinet.objects.filter(users=self.request.user)
           return RecentlyCreatedDocument.valid.all().filter(cabinets__in=cabinets)
        # return RecentlyCreatedDocument.valid.all()

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'no_results_icon': icon_document_recently_created_list,
                'no_results_text': _(
                    'This view will list the latest documents created '
                    'in the system.'
                ),
                'no_results_title': _(
                    'There are no recently created documents'
                ),
                'title': _('Recently created')
            }
        )
        return context
