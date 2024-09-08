from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from django.utils.translation import gettext_lazy as _

from mayan.apps.rest_api import serializers
from mayan.apps.user_management.serializers import UserSerializer

from .models import SavedResultset


class DummySearchResultModelSerializer(serializers.Serializer):
    """
    Empty serializer for Swagger views.
    """


class SavedResultsetSerializer(serializers.HyperlinkedModelSerializer):
    results_url = serializers.HyperlinkedIdentityField(
        label=_(message='Results URL'), lookup_url_kwarg='saved_resultset_id',
        view_name='rest_api:saved_resultset-result-list'
    )
    user = UserSerializer(
        label=_(message='User'), read_only=True
    )

    class Meta:
        extra_kwargs = {
            'url': {
                'label': _(message='URL'),
                'lookup_url_kwarg': 'saved_resultset_id',
                'view_name': 'rest_api:saved_resultset-detail'
            }
        }
        fields = (
            'app_label', 'id', 'model_name', 'result_count', 'results_url',
            'search_explainer_text', 'time_to_live', 'timestamp', 'url',
            'user'
        )
        model = SavedResultset
        read_only_fields = fields

    def create(self, validated_data):
        saved_resultset, queryset = self.context['view'].do_search_execute(
            store_resultset=True
        )

        return saved_resultset

    def validate(self, data):
        if not self.context['view'].request.user.is_authenticated:
            raise ValidationError(
                detail=_(message='User must be authenticated.')
            )

        return data


class SearchFieldSerializer(serializers.Serializer):
    field_name = serializers.CharField(
        label=_(message='Field name'), read_only=True
    )
    label = serializers.CharField(
        label=_(message='Label'), read_only=True
    )


class SearchModelSerializer(serializers.Serializer):
    app_label = serializers.CharField(
        label=_(message='App label'), read_only=True
    )
    model_name = serializers.CharField(
        label=_(message='Model name'), read_only=True
    )
    pk = serializers.CharField(
        label=_(message='Primary key'), read_only=True
    )
    search_fields = SearchFieldSerializer(
        label=_(message='Search fields'), many=True, read_only=True
    )
    url = serializers.SerializerMethodField(
        label=_(message='URL')
    )

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:searchmodel-detail', kwargs={
                'search_model_pk': instance.full_name
            }, request=self.context['request'], format=self.context['format']
        )
