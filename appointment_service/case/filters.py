import django_filters
from .models import Case

class CaseFilter(django_filters.FilterSet):
    ids = django_filters.CharFilter(method='filter_by_ids')

    class Meta:
        model = Case
        fields = ['ids']

    def filter_by_ids(self, queryset, name, value):
        id_list = value.split(',')
        return queryset.filter(id__in=id_list)