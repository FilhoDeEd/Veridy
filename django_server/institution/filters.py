import django_filters
from django.db.models import Q
from institution.models import Institution


class InstitutionFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='filter_q',
        label='Busca geral'
    )
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
        fields = ['name', 'domain', 'tax_id', 'country', 'q']

    def filter_q(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(domain__icontains=value) | Q(tax_id__icontains=value) | Q(country__icontains=value)
        )
