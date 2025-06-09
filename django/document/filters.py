import django_filters
from django.db.models import Q
from django.forms.widgets import DateInput
from document.models import Document


class DocumentFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='filter_q',
        label='Busca geral'
    )
    subject__full_name = django_filters.CharFilter(
        label='Titular',
        lookup_expr='icontains'
    )
    institution__name = django_filters.CharFilter(
        label='Instituição',
        lookup_expr='icontains'
    )
    upload_date_after = django_filters.DateFilter(
        label='Upload (desde)',
        field_name='upload_date',
        lookup_expr='date__gte',
        widget=DateInput(
            attrs={'type': 'date'}
        )
    )
    upload_date_before = django_filters.DateFilter(
        label='Upload (até)',
        field_name='upload_date',
        lookup_expr='date__lte',
        widget=DateInput(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = Document
        fields = ['subject__full_name', 'institution__name', 'upload_date_after', 'upload_date_before', 'q']

    def filter_q(self, queryset, name, value):
        return queryset.filter(
            Q(subject__full_name__icontains=value) | Q(institution__name__icontains=value)
        )
