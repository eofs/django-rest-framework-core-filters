from rest_framework.filters import BaseFilterBackend
from core_filters.filtersets import ModelFilterSet


class CoreFilterBackend(BaseFilterBackend):
    default_filter_set = ModelFilterSet

    def get_filter_class(self, view, queryset=None):
        filter_class = getattr(view, 'filter_class', None)
        filter_fields = getattr(view, 'filter_fields', None)

        if filter_class:
            filter_model = filter_class.Meta.model

            assert issubclass(queryset.model, filter_model), \
                'FilterSet model %s does not match queryset model %s' % \
                (filter_model, queryset.model)

            return filter_class

        if filter_fields:
            class AutoFilterSet(self.default_filter_set):
                class Meta:
                    model = queryset.model
                    fields = filter_fields

            return AutoFilterSet

        return None

    def filter_queryset(self, request, queryset, view):
        filter_class = self.get_filter_class(view, queryset=queryset)

        if filter_class:
            return filter_class(request.query_params, queryset=queryset).qs

        return queryset