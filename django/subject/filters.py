import django_filters
from django.db.models import Q
from subject.models import Subject


class SubjectFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='filter_q',
        label='Busca geral'
    )
    full_name = django_filters.CharFilter(
        label='Nome',
        lookup_expr='icontains'
    )
    user__email = django_filters.CharFilter(
        label='E-mail',
        lookup_expr='icontains'
    )

    class Meta:
        model = Subject
        fields = ['full_name', 'user__email', 'q']

    def filter_q(self, queryset, name, value):
        return queryset.filter(
            Q(full_name__icontains=value) | Q(user__email__icontains=value)
        )
