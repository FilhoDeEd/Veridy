import django_filters
from institution.models import Institution


class InstitutionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        label='Nome',
        lookup_expr='icontains'
    )
    domain = django_filters.CharFilter(
        label='Domínio',
        lookup_expr='icontains'
    )
    tax_id = django_filters.CharFilter(
        label='CNPJ',
        lookup_expr='icontains'
    )
    country = django_filters.CharFilter(
        label='País',
        lookup_expr='icontains'
    )

    class Meta:
        model = Institution
        fields = ['name', 'domain', 'tax_id', 'country']
