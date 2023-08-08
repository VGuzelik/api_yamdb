from django_filters import rest_framework
from reviews.models import Title


class TitleFilters(rest_framework.FilterSet):
    """Генериция фильтров для указанных полей модели Title."""

    genre = rest_framework.CharFilter(field_name='genre__slug')
    category = rest_framework.CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
