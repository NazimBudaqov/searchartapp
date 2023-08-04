from django.urls import path

from .views import *

urlpatterns = [
    path('', SectSubsectIndicaView.as_view(), name='get-default-data'),
    path('countries-data/<str:indicator_name>/', CountriesView.as_view(), name='get-related-countries'),
    path('available-years/', AvailableYearsView.as_view(), name='get-available-years'),
    path('ranks/', AvailableRanksView.as_view(), name='get-available-ranks'),
    
    #?year1=2010&year2=2020&ranks=5,172
    path('diagramsData/', AllDiagramsView.as_view(),name='years-data'),
    
    path('by_amount/', AmountView.as_view(), name='diagram1-only'),
    path('rank_diff/', RankDifferenceView.as_view(),name='diagram2-only'),
    path('years_data/', RankAmountDiagrams.as_view(),name='diagram3&4-only'),

    path('import/', ImportView.as_view(), name='import-data'),
]
