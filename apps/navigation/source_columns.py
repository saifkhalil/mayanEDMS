import logging

from django.contrib.admin.utils import help_text_for_field, label_for_field
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.db.models.constants import LOOKUP_SEP
from django.template import Variable, VariableDoesNotExist
from django.utils.translation import gettext_lazy as _

from mayan.apps.common.utils import get_related_field, resolve_attribute
from mayan.apps.views.icons import icon_sort_down, icon_sort_up
from mayan.apps.views.literals import (
    TEXT_SORT_FIELD_PARAMETER, TEXT_SORT_FIELD_VARIABLE_NAME
)

from .class_mixins import TemplateObjectMixin
from .column_widgets import SourceColumnLinkWidget

logger = logging.getLogger(name=__name__)


class SourceColumn(TemplateObjectMixin):
    _registry = {}

    @staticmethod
    def get_attribute_recursive(attribute, model):
        """
        Walk over the double underscore (__) separated path to the last
        field. Returns the field name and the corresponding model class.
        Used to introspect the label or short_description of a model's
        attribute.
        """
        last_model = model
        for part in attribute.split(LOOKUP_SEP):
            last_model = model
            try:
                field = model._meta.get_field(field_name=part)
            except FieldDoesNotExist:
                break
            else:
                model = field.related_model or field.model

        return (part, last_model)

    @staticmethod
    def sort(columns):
        columns.sort(key=lambda x: x.order)
        return columns

    @classmethod
    def get_column_matches(cls, source):
        if source == [] or source == ():
            # There are no objects to match and the object type is not
            # a queryset where the model can be obtained from empty values.
            # Short circuit and return empty columns.
            return ()

        columns = []

        try:
            # Try it as a queryset.
            model = source.model
        except AttributeError:
            try:
                # Try it as a list.
                item = source[0]
            except TypeError:
                # Neither a queryset nor a list.
                try:
                    # Try as a model instance or model.
                    model = source._meta.model
                except AttributeError:
                    # Not a model instance.

                    try:
                        super_class_list = source.__mro__[:-1]
                    except AttributeError:
                        # Is not a class.

                        # Try as subclass instance, check the class hierarchy.
                        for super_class in source.__class__.__mro__[:-1]:
                            columns.extend(
                                cls._registry.get(
                                    super_class, ()
                                )
                            )
                    else:
                        # Try as a subclass.
                        for super_class in super_class_list:
                            columns.extend(
                                cls._registry.get(
                                    super_class, ()
                                )
                            )

                    return columns
                else:
                    # Get model columns.
                    columns.extend(
                        cls._registry.get(
                            model, ()
                        )
                    )

                    # Get proxy columns.
                    # Remove the columns explicitly excluded.
                    # Execute after the root model columns to allow a proxy
                    # to override an existing column.
                    proxy_columns = cls._registry.get(
                        model._meta.proxy_for_model, ()
                    )
                    for proxy_column in proxy_columns:
                        if model not in proxy_column.excludes:
                            columns.append(proxy_column)

                    return columns
            else:
                # It is a list.
                return cls.get_column_matches(source=item)
        else:
            # It is a queryset.
            return cls.get_column_matches(source=model)

    @classmethod
    def get_for_source(
        cls, source, exclude_identifier=False, names=None,
        only_identifier=False
    ):
        # Process columns as a set to avoid duplicate resolved column
        # detection code.
        columns = cls.get_column_matches(source=source)

        if exclude_identifier:
            columns = [
                column for column in columns if not column.is_identifier
            ]
        else:
            # exclude_identifier and only_identifier and mutually exclusive.
            if only_identifier:
                for column in columns:
                    if column.is_identifier:
                        return (column,)

                # There is no column with the identifier marker.
                return ()

        if names is not None:
            indexed_columns = {
                column.name: column for column in columns
            }

            return [
                indexed_columns[name] for name in names
            ]

        columns = SourceColumn.sort(columns=columns)

        return columns

    @classmethod
    def get_sortable_for_source(cls, source):
        result = []
        for column in cls.get_for_source(source=source):
            if column.is_sortable:
                result.append(column)

        return result

    def __init__(
        self, source, attribute=None, empty_value=None, func=None,
        help_text=None, html_extra_classes=None, include_label=False,
        is_attribute_absolute_url=False, is_object_absolute_url=False,
        is_identifier=False, is_sortable=False, kwargs=None, label=None,
        name=None, order=None, sort_field=None, widget=None
    ):
        """
        name: optional unique identifier for this source column for the
        specified source.
        """
        self._label = label
        self._help_text = help_text
        self.source = source
        self.attribute = attribute
        self.empty_value = empty_value
        self.excludes = set()
        self.func = func
        self.html_extra_classes = html_extra_classes or ''
        self.include_label = include_label
        self.is_attribute_absolute_url = is_attribute_absolute_url
        self.is_object_absolute_url = is_object_absolute_url
        self.is_identifier = is_identifier
        self.is_sortable = is_sortable
        self._kwargs = kwargs or {}
        self.name = name
        self.order = order or 0
        self.sort_field = sort_field
        self.widget = widget

        if self.is_attribute_absolute_url or self.is_object_absolute_url:
            if not self.widget:
                self.widget = SourceColumnLinkWidget

        self.__class__._registry.setdefault(
            source, []
        )
        self.__class__._registry[source].append(self)

        self._calculate_label()
        self._calculate_help_text()
        if self.is_sortable:
            field_name = self.sort_field or self.attribute
            try:
                get_related_field(
                    model=self.source, related_field_name=field_name
                )
            except FieldDoesNotExist as exception:
                raise ImproperlyConfigured(
                    '"{}" is not a field of "{}", cannot be used as a '
                    'sortable column.'.format(field_name, self.source)
                ) from exception

    def _calculate_help_text(self):
        if not self._help_text:
            if self.attribute:
                try:
                    attribute = resolve_attribute(
                        obj=self.source, attribute=self.attribute
                    )
                    self._help_text = getattr(attribute, 'help_text')
                except AttributeError:
                    try:
                        name, model = SourceColumn.get_attribute_recursive(
                            attribute=self.attribute,
                            model=self.source._meta.model
                        )
                        self._help_text = help_text_for_field(
                            model=model, name=name
                        )
                    except AttributeError:
                        self._help_text = None

        self.help_text = self._help_text

    def _calculate_label(self):
        if not self._label:
            if self.attribute:
                try:
                    attribute = resolve_attribute(
                        attribute=self.attribute, obj=self.source
                    )
                    self._label = getattr(attribute, 'short_description')
                except AttributeError:
                    try:
                        name, model = SourceColumn.get_attribute_recursive(
                            attribute=self.attribute,
                            model=self.source._meta.model
                        )
                        self._label = label_for_field(
                            model=model, name=name
                        )
                    except AttributeError:
                        self._label = self.attribute
            else:
                self._label = getattr(
                    self.func, 'short_description', _(
                        message='Unnamed function'
                    )
                )

        self.label = self._label

    def add_exclude(self, source):
        self.excludes.add(source)

    def do_kwargs_resolve(self, context):
        try:
            kwargs = self._kwargs(context)
        except TypeError:
            # Is not a callable.
            kwargs = self._kwargs

        return {
            key: Variable(var=value).resolve(context=context) for key, value in kwargs.items()
        }

    def get_absolute_url(self, obj):
        if self.is_object_absolute_url:
            return obj.get_absolute_url()
        elif self.is_attribute_absolute_url:
            result = resolve_attribute(
                attribute=self.attribute, kwargs=self.kwargs,
                obj=obj
            )
            if result:
                return result.get_absolute_url()

    def get_is_active_sort_field(self, context, reverse=False):
        previous_sort_fields = self.get_previous_sort_fields(context=context)
        sort_field = self.get_sort_field()

        if len(previous_sort_fields) == 1:
            if reverse:
                return '-{}'.format(sort_field) in previous_sort_fields
            else:
                return sort_field in previous_sort_fields

    def get_previous_sort_fields(self, context):
        previous_sort_fields = context.get(
            TEXT_SORT_FIELD_VARIABLE_NAME, None
        )

        if previous_sort_fields:
            previous_sort_fields = previous_sort_fields.split(',')
        else:
            previous_sort_fields = ()

        return previous_sort_fields

    def get_sort_field(self):
        if self.sort_field:
            return self.sort_field
        else:
            return self.attribute

    def get_sort_field_querystring(
        self, context, order=None, single_column=False
    ):
        request = self.get_request(context=context)

        # Get an mutable copy that can be modified.
        querystring = request.GET.copy()

        sort_field = self.get_sort_field()

        ascending = sort_field
        descending = '-{}'.format(sort_field)

        previous_sort_fields = list(
            self.get_previous_sort_fields(context=context)
        )

        if single_column:
            # Create a new list Remove all other fields from the list.
            if order == 'ascending':
                previous_sort_fields = []
            elif order == 'descending':
                previous_sort_fields = [ascending]
            elif order == 'clear':
                previous_sort_fields = [descending]
            else:
                previous_sort_fields = list(
                    set(previous_sort_fields).intersection(
                        (ascending, descending)
                    )
                )

        if ascending not in previous_sort_fields and descending not in previous_sort_fields:
            previous_sort_fields.append(ascending)
        elif descending in previous_sort_fields:
            previous_sort_fields.remove(descending)
        else:
            previous_sort_fields.insert(
                previous_sort_fields.index(ascending), descending
            )
            previous_sort_fields.remove(ascending)

        querystring[TEXT_SORT_FIELD_PARAMETER] = ','.join(previous_sort_fields)

        return '?{}'.format(
            querystring.urlencode()
        )

    def get_sort_icon(self, context):
        previous_sort_fields = self.get_previous_sort_fields(context=context)
        sort_field = self.get_sort_field()

        if sort_field in previous_sort_fields:
            return icon_sort_down
        elif '-{}'.format(sort_field) in previous_sort_fields:
            return icon_sort_up

    def resolve(self, context):
        kwargs = self.do_kwargs_resolve(context=context)

        if self.attribute:
            try:
                result = resolve_attribute(
                    attribute=self.attribute, kwargs=kwargs,
                    obj=context['object']
                )
            except Exception as exception:
                raise AttributeError(
                    'Unable to resolve SourceColumn attribute `{}` for object `{}`; {}.'.format(
                        self.attribute, context['object'], exception
                    )
                ) from exception
        elif self.func:
            result = self.func(context=context, **kwargs)
        else:
            result = context['object']

        self.absolute_url = self.get_absolute_url(
            obj=context['object']
        )
        if self.widget:
            try:
                request = self.get_request(context=context)
            except VariableDoesNotExist:
                """
                Don't attempt to render and return the value if any.
                """
            else:
                widget_instance = self.widget(
                    column=self, request=request, value=result
                )
                return widget_instance.render()

        if not result:
            if self.empty_value:
                return self.empty_value
            else:
                return result
        else:
            return result
