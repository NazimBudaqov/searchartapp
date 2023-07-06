from django.urls import path
from .views import ApiGetData,import_data

urlpatterns = [
    #1
    path('', ApiGetData.as_view({'get':'get'}), name='get-default-data'),
    path('countries-data/<str:indicator_name>/', ApiGetData.as_view({'get':'get_related_countries_data'}), name='get-countries-and-ranks'),
    path('available-years/<str:indicator_name>/<str:country_name>/', ApiGetData.as_view({'get':'get_available_years'}), name='get-years'),
    #2 #?year1=2010&year2=2020&ranks=4,5
    path('<str:indicator_name>/<str:country_name>/', ApiGetData.as_view({'get':'get_diagrams_data'}),name='years-data'),
    path('request/<str:indicator_name>/<str:country_name>/', ApiGetData.as_view({'get':'get_diagram_2_data'}),name='update-diagram2-data'),
    #3
    path('import/', import_data, name='import-data'),
]

# path('2/<str:indicator_name>/<str:country_name>/', ApiGetData.as_view({'get':'get_data_by_indicator'}), name='indicator-data'),
