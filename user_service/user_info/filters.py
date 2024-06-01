import django_filters
from authentication.models import Account

class AccountFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='iexact')
    role = django_filters.ChoiceFilter(choices=Account.RoleInAccount.choices)
    
    class Meta:
        model = Account
        fields = ['username', 'role']
