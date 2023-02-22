from django_filters import rest_framework as filters

from reviews.models import Title


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CustomFilter1(filters.FilterSet):
    name = filters.Filter()
    genre = CharFilterInFilter(field_name='genre__slug', lookup_expr='in')

    class Meta:
        model = Title
        fields = ('name', 'genre',)


class CustomFilter2(filters.FilterSet):
    year = filters.Filter()
    category = CharFilterInFilter(field_name='category__slug', lookup_expr='in')

    class Meta:
        model = Title
        fields = ('year', 'category',)


class CustomFilter(CustomFilter1, CustomFilter2):
    pass
