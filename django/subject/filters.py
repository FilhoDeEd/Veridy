import django_filters
from subject.models import Subject


class SubjectFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(
        label='Nome',
        lookup_expr='icontains'
    )

    class Meta:
        model = Subject
        fields = ['full_name']
