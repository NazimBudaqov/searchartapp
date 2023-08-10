from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from ...models import MainData

class RankDifferenceView(APIView):
    #diagram 2 - rank difference of countries by given indciator and years

    # can be accessed through both all_diagrams_data() requests and individual 
    # requests(to change diagram by selectable year1 and year2 values) 
    
    def get(self='',request='', def_request=''):
        if request!='':
            pass
        else:
            if def_request!='':
                request=def_request
            else:
                return "false request"
        
        indicator_name =  request.GET.get('indicator')
        countries = str(request.GET.get('countries')).split(';')
        year1 = int(request.GET.get('year1'))
        
        queryset = MainData.objects.select_related('indicator').filter(indicator__indicatorName=indicator_name)

        if request.GET.get('year2'):
            year2 = int(request.GET.get('year2'))
        else:
            years = set()
            for data in queryset.filter(country__countryName__in=countries):
                for item in data.json_data:
                    years.add(item['year'])
            year2 = max(years)        

        each_country_year_data = []
        try:
            # pass
            for data in queryset.select_related('country').filter(country__countryName__in=countries):
                rank1 = 0
                rank2 = 0
                amount1 = 0
                amount2= 0
                for item in data.json_data:
                    if item['year'] == year1:
                        rank1 = item['rank']
                        amount1 = item['amount']
                    if item['year'] == year2:
                        rank2 = item['rank']
                        amount2 = item['amount']
                    else:
                        continue

                if rank1 != 0 and rank2 != 0:
                    country_obj = model_to_dict(data.country)
                    each_country_year_data.append(
                        {
                            'country':country_obj['countryName'],
                            'country_code':country_obj['country_code'],
                            'country_code_2':country_obj['country_code_2'],
                            'first_rank' : rank1,
                            'first_amount' : amount1,
                            'second_rank' : rank2,
                            'second_amount' : amount2,
                            'rank_difference' : (rank2-rank1),
                            }
                    )
               
        except ObjectDoesNotExist:
            pass

        diagram2 = {
                "indicator" : indicator_name,
                "first_year" : year1,
                "second_year" : year2,
                "countries" : each_country_year_data
                }
        
        if request!='' and request != def_request:
            return Response(diagram2, status=status.HTTP_200_OK)
        else:
            if def_request!='':
                return diagram2
