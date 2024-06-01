import django_filters
from .models import Bill

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class BillFilter(django_filters.FilterSet):
    ammount = django_filters.NumberFilter()
    case__in = NumberInFilter(field_name='case', lookup_expr='in')

    class Meta:
        model = Bill
        fields = ['case__in', 'ammount']