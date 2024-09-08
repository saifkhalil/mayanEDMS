from functools import cache

from django.conf import settings
from django.contrib.admin.utils import reverse_field_path
from django.core.exceptions import ImproperlyConfigured

from .literals import DJANGO_SQLITE_BACKEND


def check_for_sqlite():
    return settings.DATABASES['default']['ENGINE'] == DJANGO_SQLITE_BACKEND and settings.DEBUG is False


def check_queryset(view, queryset):
    """
    Validate that a view queryset is usable.
    """
    try:
        queryset.query
    except AttributeError:
        # Check if it is an iterable.
        try:
            iter(queryset)
        except TypeError as exception:
            raise ImproperlyConfigured(
                'Queryset `{}` of view `{}` is not a valid queryset.'.format(
                    queryset, view.__class__
                )
            ) from exception
        else:
            return queryset
    else:
        return queryset


def instance_list_to_queryset(instance_list):
    manager = instance_list[0]._meta.default_manager

    return manager.filter(
        pk__in=[instance.pk for instance in instance_list]
    )


def _get_model_ordering_fields(
    model, exclude=None, prefix=None, separator='__'
):
    if prefix:
        prefix_string = '{}{}'.format(prefix, separator)
    else:
        prefix_string = ''

    model_ordering_fields = getattr(
        model, '_ordering_fields', ()
    )

    model_ordering_fields += (model._meta.pk.name,)

    for field_name in sorted(model_ordering_fields):
        yield '{}{}'.format(prefix_string, field_name)

    for field in model._meta.fields:
        if field.concrete:
            related_model, path = reverse_field_path(
                model=model, path=field.name
            )

            if path and related_model != exclude:
                prefix_related = '{}{}'.format(prefix_string, field.name)

                yield from _get_model_ordering_fields(
                    exclude=model, model=related_model, prefix=prefix_related
                )


@cache
def get_model_ordering_fields(model):
    iterable_field_list = _get_model_ordering_fields(model=model)
    field_list = tuple(iterable_field_list)
    return sorted(field_list)
