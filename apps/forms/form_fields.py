from django.forms.fields import *  # NOQA
from django.forms.fields import __all__ as django_forms_fields_all
from django.forms.fields import ChoiceField, MultipleChoiceField
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField

from .field_mixins import (
    FormFieldMixinFilteredQueryset, ModelFieldMixinFilteredQuerySet
)

__all__ = django_forms_fields_all + (
    'FormFieldFilteredModelChoice', 'FormFieldFilteredModelChoiceMultiple',
    'ModelFormFieldFilteredModelChoice',
    'ModelFormFieldFilteredModelMultipleChoice'
)


class FormFieldFilteredModelChoice(
    FormFieldMixinFilteredQueryset, ChoiceField
):
    """Single selection filtered model choice field."""


class FormFieldFilteredModelChoiceMultiple(
    FormFieldMixinFilteredQueryset, MultipleChoiceField
):
    """Multiole selection filtered model choice field."""


class ModelFormFieldFilteredModelChoice(
    ModelFieldMixinFilteredQuerySet, ModelChoiceField
):
    """Single selection filtered model choice field."""


class ModelFormFieldFilteredModelMultipleChoice(
    ModelFieldMixinFilteredQuerySet, ModelMultipleChoiceField
):
    """Multiple selection filtered model choice field."""
