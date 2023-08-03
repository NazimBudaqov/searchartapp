from django.urls import path

from .views import *

urlpatterns = [
    path('', SelectorDataView.as_view({'get':'get'}), name='get-default-data'),
    path('countries-data/<str:indicator_name>/', SelectorDataView.as_view({'get':'get_related_countries_data'}), name='get-related-countries'),
    path('available-years/<str:indicator_name>/<str:country_name>/', SelectorDataView.as_view({'get':'get_available_years'}), name='get-available-years'),
    
    #?year1=2010&year2=2020&ranks=5,172
    path('diagramsData/', AllDiagramsView.as_view(),name='years-data'),
    
    path('by_amount/', AmountView.as_view(), name='diagram1-only'),
    path('rank_diff/', RankDifferenceView.as_view(),name='diagram2-only'),
    path('years_data/', RankAmountDiagrams.as_view(),name='diagram3&4-only'),

    path('import/', ImportView.as_view(), name='import-data'),
]
