from django.db.models import Min,Max
from django.db.models import Prefetch

from rest_framework.response import Response
from rest_framework import viewsets

from ...models import Sector, Subsector, Country, YearData 

#api - get dashboard data
class SelectorDataView(viewsets.ViewSet):
    def get(self, request):
        sectors_data = (
            Sector.objects.prefetch_related(
                Prefetch('subsectors', queryset=Subsector.objects.prefetch_related('indicator'))
            )
            .values('sectorName', 'subsectors__subSectorName', 'subsectors__indicator__indicatorName')
        )
        sectors = {}
        
        for sector in sectors_data:
            sector_name = sector['sectorName']
            subsector_name = sector['subsectors__subSectorName']
            indicator_name = sector['subsectors__indicator__indicatorName']

            if sector_name not in sectors:
                sectors[sector_name] = {}
            
            if subsector_name not in sectors[sector_name]:
                sectors[sector_name][subsector_name] = []
            
            sectors[sector_name][subsector_name].append(indicator_name)
        data = {
            "sectors": sectors,
            "default_choices":[Sector.objects.get(sectorName='Economy').id,0,0]
        }

        return Response(data)
    
    #returns countries and extreme ranks for given indicator and year
    def get_related_countries_data(self,request,indicator_name):
        year = request.GET.get("year")
        
        countries = []
        countries_data = Country.objects.order_by('countryName').filter(indicator__indicatorName=indicator_name).distinct()
        for country in countries_data:
            countries.append(country.countryName)
        
        if year is not None:
            rank_list = (
                YearData.objects.filter(indicator__indicatorName=indicator_name,year=year)
                .aggregate(min_rank=Min('rank'), max_rank=Max('rank'))
            )
            if rank_list['min_rank'] is None:
                rank_list = {
                    'min_rank': 'no rank data in this year',     
                    'max_rank': 'no rank data in this year'     
                }
        else:
            rank_list = {
            'min_rank':'input year value',     
            'max_rank':'input year value'     
        }
                
        data = {
            "countries": countries,
            'min_rank': rank_list['min_rank'],
            'max_rank': rank_list['max_rank']
        }
        
        return Response(data)
    
    #returns year for corresponding countries in given indicator
    def get_available_years(self,request,indicator_name,country_name): 
        years = []
        for country in country_name.split(','):
            year_data = YearData.objects\
                .filter(indicator__indicatorName=indicator_name,country__countryName = country)\
                .values()
        for year in year_data:
            years.append(year['year'])
        return Response(years)
    