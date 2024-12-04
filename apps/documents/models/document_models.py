import uuid

from django.db import models, transaction
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.common.signals import signal_mayan_pre_save
from mayan.apps.events.classes import EventManagerSave
from mayan.apps.events.decorators import method_event
from django.conf import settings
from ..events import (
    event_document_created, event_document_edited,
    event_document_trashed, event_trashed_document_deleted
)

from ..literals import DEFAULT_LANGUAGE
from ..managers import (
    DocumentManager, TrashCanManager, ValidDocumentManager,
    ValidRecentlyCreatedDocumentManager
)

from .document_model_mixins import DocumentBusinessLogicMixin
from .document_type_models import DocumentType
from .model_mixins import HooksModelMixin

__all__ = ('Document', 'DocumentSearchResult',)


class Document(
    DocumentBusinessLogicMixin, ExtraDataModelMixin, HooksModelMixin,
    models.Model
):
    """
    Defines a single document with it's fields and properties
    Fields:
    * uuid - UUID of a document, universally Unique ID. An unique identifier
    generated for each document. No two documents can ever have the same UUID.
    This ID is generated automatically.
    """
    _hooks_pre_create = []

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, help_text=_(
            'UUID of a document, universally Unique ID. An unique identifier '
            'generated for each document.'
        ), verbose_name=_('UUID')
    )
    document_type = models.ForeignKey(
        help_text=_('The document type of the document.'),
        on_delete=models.CASCADE, related_name='documents', to=DocumentType,
        verbose_name=_('Document type')
    )
    label = models.CharField(
        blank=True, db_index=True, default='', max_length=255,
        help_text=_(
            'A short text identifying the document. By default, will be '
            'set to the filename of the first file uploaded to the document.'
        ),
        verbose_name=_('Label')
    )
    description = models.TextField(
        blank=True, default='', help_text=_(
            'An optional short text describing a document.'
        ), verbose_name=_('Description')
    )
    datetime_created = models.DateTimeField(
        auto_now_add=True, db_index=True, help_text=_(
            'The date and time of the document creation.'
        ), verbose_name=_('Created')
    )
    language = models.CharField(
        blank=True, default=DEFAULT_LANGUAGE, help_text=_(
            'The primary language in the document.'
        ), max_length=8, verbose_name=_('Language')
    )
    in_trash = models.BooleanField(
        db_index=True, default=False, help_text=_(
            'Whether or not this document is in the trash.'
        ), editable=False, verbose_name=_('In trash?')
    )
    trashed_date_time = models.DateTimeField(
        blank=True, editable=True, help_text=_(
            'The server date and time when the document was moved to the '
            'trash.'
        ), null=True, verbose_name=_('Date and time trashed')
    )
    is_stub = models.BooleanField(
        db_index=True, default=True, editable=False, help_text=_(
            'A document stub is a document with an entry on the database but '
            'no file uploaded. This could be an interrupted upload or a '
            'deferred upload via the API.'
        ), verbose_name=_('Is stub?')
    )

    create_by = models.ForeignKey(
        on_delete=models.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL,blank=True,null=True,
        verbose_name=_('Created By')
    )
    from_cabinet = models.CharField(blank=True, default='', help_text=_('From Cabinet.'), max_length=200, verbose_name=_('Cabinet'))
    number = models.IntegerField(default=0,verbose_name=_('Document Number'),help_text=_("Document Number"))


    objects = DocumentManager()
    trash = TrashCanManager()
    valid = ValidDocumentManager()

    class Meta:
        ordering = ('label',)
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')

    def __str__(self):
        return self.get_label()

    def delete(self, *args, **kwargs):
        to_trash = kwargs.pop('to_trash', True)
        user = self.__dict__.pop('_event_actor', None)

        if not self.in_trash and to_trash:
            self.in_trash = True
            self.trashed_date_time = now()
            with transaction.atomic():
                self._event_ignore = True
                self.save(
                    update_fields=('in_trash', 'trashed_date_time')
                )

            event_document_trashed.commit(actor=user, target=self)
        else:
            with transaction.atomic():
                for document_file in self.files.all():
                    document_file.delete()

                super().delete(*args, **kwargs)

            event_trashed_document_deleted.commit(
                actor=user, target=self.document_type
            )

    def get_absolute_url(self):
        return reverse(
            viewname='documents:document_preview', kwargs={
                'document_id': self.pk
            }
        )

    def natural_key(self):
        return (self.uuid,)
    natural_key.dependencies = ['documents.DocumentType']

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_document_created,
            'action_object': 'document_type',
            'target': 'self'
        },
        edited={
            'event': event_document_edited,
            'target': 'self'
        }
    )
    def save(self, *args, **kwargs):
        user = self.__dict__.pop('_event_actor', None)
        new_document = not self.pk

        signal_mayan_pre_save.send(
            instance=self, sender=Document, user=user
        )
        self.create_by = user
        try:
            mycabinet = user.user_cabinets.first()
            mycabinet_label = str(mycabinet.label)
            doc_type_flow = self.document_type.doc_flow
            if doc_type_flow == 'Incomming':
                number = mycabinet.incomming
                self.number = number
                mycabinet.incomming = number+1
                mycabinet.save()
            if doc_type_flow == 'Outgoing':
                number = mycabinet.outgoing
                self.number = number
                mycabinet.outgoing = number+1
                mycabinet.save()
            self.from_cabinet = mycabinet_label
        except:
            self.from_cabinet = ''
        super().save(*args, **kwargs)

        if new_document:
            if user:
                self.add_as_recent_document_for_user(user=user)
                

class DocumentSearchResult(Document):
    class Meta:
        proxy = True


class RecentlyCreatedDocument(Document):
    objects = models.Manager()
    valid = ValidRecentlyCreatedDocumentManager()

    class Meta:
        proxy = True
