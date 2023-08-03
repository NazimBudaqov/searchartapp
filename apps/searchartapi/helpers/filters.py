from django_filters import rest_framework as filters
from apps.searchartapi.models import Country,YearData,Indicator

class YearDataFilter(filters.FilterSet):
    ranks = filters.RangeFilter(field_name='rank')
    year1 = filters.NumberFilter(field_name='year')
    countries = filters.CharFilter(field_name='country', method='filter_by_country')    
    indicator = filters.CharFilter(field_name='indicator')

    class Meta:
        model = YearData
        fields = []

    def filter_by_country(self, queryset, name, value):
        country_names = value.split(',')
        return queryset.filter(country__in=country_names)
