from django.apps import apps
from django.utils.translation import gettext_lazy as _
from mayan.apps.user_management.permissions import permission_user_view
from mayan.apps.user_management.querysets import get_user_queryset
from .events import event_cabinet_edited

def method_document_get_cabinets(self, permission, user):
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )
    DocumentCabinet = apps.get_model(
        app_label='cabinets', model_name='DocumentCabinet'
    )

    return AccessControlList.objects.restrict_queryset(
        permission=permission, queryset=DocumentCabinet.objects.filter(
            documents=self
        ), user=user
    )


method_document_get_cabinets.help_text = _(
    'Return a list of cabinets containing the document.'
)
method_document_get_cabinets.short_description = _('get_cabinets()')

def method_cabinet_get_users(self, user, permission=permission_user_view):
   AccessControlList = apps.get_model(
       app_label='acls', model_name='AccessControlList'
   )


   return AccessControlList.objects.restrict_queryset(
       permission=permission, queryset=get_user_queryset().filter(
           id__in=self.users.all()
       ), user=user
   )

def method_cabinet_users_add(self, queryset, user=None):
   for model_instance in queryset:
       self.users.add(model_instance)
       event_cabinet_edited.commit(
           action_object=model_instance, actor=user, target=self
       )


def method_cabinet_users_remove(self, queryset, user=None):
   for model_instance in queryset:
       self.users.remove(model_instance)
       event_cabinet_edited.commit(
           action_object=model_instance, actor=user, target=self
       )
