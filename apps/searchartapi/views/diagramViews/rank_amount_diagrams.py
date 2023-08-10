from ...models import MainData

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.forms import model_to_dict

# diagram 3 and 4 display country name,code and code_2 and change of their ranks and amounts  
# data for chosen countries over all available years, by given indicator.
class RankAmountDiagrams(APIView):
    def get(self='',request='',def_request=''):
        if request!='':
            pass
        else:
            if def_request!='':
                request=def_request
            else:
                return "false request"
        
        indicator_name =  request.GET.get('indicator')
        countries = str(request.GET.get('countries')).split(';')
        year = int(request.GET.get('year1'))
        ranks = list(map(int,str(request.GET.get('ranks')).split(',')))

        queryset = MainData.objects.select_related('indicator','country')\
        .filter(indicator__indicatorName=indicator_name,)

        result = {}
        amount_list = []
        rank_list = []
        year_list = set()
        result['countries_data'] = []
        
        countries_filtered_by_rank = []
        for data in queryset.filter(country__countryName__in=countries):
            for item in data.json_data:
                if item['year'] == year and ranks[0] <= item['rank'] <= ranks[1]+1:
                    countries_filtered_by_rank.append(model_to_dict(data.country)['countryName']) #(model_to_dict(data.country)['countryName'],'rank',item['rank'],'year',item['year'])
        
        for data in queryset.filter(country__countryName__in=countries_filtered_by_rank):
            country_obj = model_to_dict(data.country)
            result['countries_data'].append({'country':[]})
            for item in data.json_data:
                if item['rank'] in range(ranks[0],ranks[1]+1):
                    result['countries_data'][-1]['country'].append(
                        {
                            'Country':country_obj['countryName'],
                            'Country_code_2':country_obj['country_code_2'],
                            'Year': item['year'],
                            'Rank': item['rank'],
                            'Amount': item['amount']
                            }
                    )

                    amount_list.append(item['amount'])
                    rank_list.append(item['rank'])
                    year_list.add(item['year'])

        # result['countries_data'] = sorted(result['countries_data'])
        result['min_rank'] = min(ranks,default="EMPTY")
        result['max_rank'] = max(ranks,default="EMPTY")
        result['min_amount'] = min(amount_list,default="EMPTY")
        result['max_amount'] = max(amount_list,default="EMPTY")
        result['year1'] = min(year_list,default="EMPTY")
        result['year2'] = max(year_list,default="EMPTY")


        if request!='' and request != def_request:
            return Response(result, status=status.HTTP_200_OK)
        else:
            if def_request!='':
                return result
