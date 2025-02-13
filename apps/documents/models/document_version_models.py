from django.db import models, transaction
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.events.classes import (
    EventManagerMethodAfter, EventManagerSave
)
from mayan.apps.events.decorators import method_event

from ..events import (
    event_document_version_created, event_document_version_deleted,
    event_document_version_edited
)
from ..managers import ValidDocumentVersionManager

from .document_models import Document
from .document_version_model_mixins import DocumentVersionBusinessLogicMixin

__all__ = ('DocumentVersion', 'DocumentVersionSearchResult')


class DocumentVersion(
    DocumentVersionBusinessLogicMixin, ExtraDataModelMixin, models.Model
):
    document = models.ForeignKey(
        on_delete=models.CASCADE, related_name='versions', to=Document,
        verbose_name=_('Document')
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, db_index=True, help_text=_(
            'The server date and time when the document version was created.'
        ), verbose_name=_('Timestamp')
    )
    comment = models.TextField(
        blank=True, default='', help_text=_(
            'An optional short text describing the document version.'
        ), verbose_name=_('Comment')
    )
    active = models.BooleanField(
        default=True, help_text=_(
            'Determines the active version of the document.'
        ), verbose_name=_('Active')
    )

    objects = models.Manager()
    valid = ValidDocumentVersionManager()

    class Meta:
        ordering = ('timestamp',)
        verbose_name = _('Document version')
        verbose_name_plural = _('Document versions')

    def __str__(self):
        return self.get_label()

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_document_version_deleted,
        target='document',
    )
    def delete(self, *args, **kwargs):
        for page in self.pages.all():
            page.delete()

        self.cache_partition.delete()

        return super().delete(*args, **kwargs)

    def get_absolute_re_path(self):
        return reverse(
            viewname='documents:document_version_preview', kwargs={
                'document_version_id': self.pk
            }
        )

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_document_version_created,
            'action_object': 'document',
            'target': 'self'
        },
        edited={
            'event': event_document_version_edited,
            'action_object': 'document',
            'target': 'self'
        }
    )
    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.active:
                self.active_set(save=False)

            return super().save(*args, **kwargs)


class DocumentVersionSearchResult(DocumentVersion):
    class Meta:
        proxy = True
