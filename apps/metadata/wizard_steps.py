from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from mayan.apps.sources.classes import DocumentCreateWizardStep
from mayan.apps.sources.wizard_steps import DocumentCreateWizardStepDocumentType

from .forms import DocumentMetadataFormSet
from .utils import (
    decode_metadata_from_query_string, save_metadata_list
)


class DocumentCreateWizardStepMetadata(DocumentCreateWizardStep):
    form_class = DocumentMetadataFormSet
    label = _('Enter document metadata')
    name = 'metadata_entry'
    number = 1

    @classmethod
    def condition(cls, wizard):
        """
        Skip step if document type has no associated metadata
        """
        cleaned_data = wizard.get_cleaned_data_for_step(
            step=DocumentCreateWizardStepDocumentType.name
        ) or {}

        document_type = cleaned_data.get('document_type')

        if document_type:
            return document_type.metadata.exists()

    @classmethod
    def get_form_initial(cls, wizard):
        initial = []

        step_data = wizard.get_cleaned_data_for_step(
            step=DocumentCreateWizardStepDocumentType.name
        )
        if step_data:
            document_type = step_data['document_type']
            for document_type_metadata_type in document_type.metadata.all():
                initial.append(
                    {
                        'document_type': document_type,
                        'metadata_type': document_type_metadata_type.metadata_type
                    }
                )

        return initial

    @classmethod
    def done(cls, wizard):
        result = {}
        cleaned_data = wizard.get_cleaned_data_for_step(step=cls.name)
        if cleaned_data:
            for index, metadata in enumerate(iterable=wizard.get_cleaned_data_for_step(step=cls.name)):
                if metadata.get('update'):
                    result[
                        'metadata{}_metadata_type_id'.format(index)
                    ] = metadata['metadata_type_id']
                    result[
                        'metadata{}_value'.format(index)
                    ] = metadata['value']

        return result

    @classmethod
    def step_post_upload_process(
        cls, document, source_id, user_id, extra_data=None, query_string=None
    ):
        User = get_user_model()

        metadata_dict_list = decode_metadata_from_query_string(
            query_string=query_string
        )

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            user = None

        if metadata_dict_list:
            save_metadata_list(
                create=True, document=document,
                metadata_list=metadata_dict_list, user=user
            )


DocumentCreateWizardStep.register(step=DocumentCreateWizardStepMetadata)
