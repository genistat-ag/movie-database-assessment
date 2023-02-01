from django_filters import rest_framework as filters
from .models import Movie


# We create filters for each field we want to be able to filter on
class MovieFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    genre = filters.CharFilter(lookup_expr='icontains')
    year = filters.NumberFilter()
    year__gt = filters.NumberFilter(field_name='year' )
    year__lt = filters.NumberFilter(field_name='year')
    creator__username = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = ['title', 'genre', 'year', 'year__gt', 'year__lt', 'creator__username']

