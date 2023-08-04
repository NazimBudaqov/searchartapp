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
        countries = str(request.GET.get('countries')).split(',')
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

        print('amounts: ', amount_list)
        print('max_rank: ',result['max_rank'], 'min_rank: ', result['min_rank'])

        if request!='' and request != def_request:
            return Response(result, status=status.HTTP_200_OK)
        else:
            if def_request!='':
                return result

        # year_data = []
        # rank_list = []
        # amount_list = []
        # year_list = []

        # for country in countries:
        #     year_data.append(YearData.objects.filter(country = country, 
        #                                              indicator = indicator_name,
        #                                              year__in=YearData.objects.filter(country = country, 
        #                                                                               indicator = indicator_name)
        #                                                                               .values_list('year'))
        #                                                                               .values_list('rank','amount','year'))
        # for queryset in year_data:
        #     for value in queryset:
        #         rank_list.append(value[0])
        #         amount_list.append(value[1])
        #         year_list.append(value[2])
        
        # data = {'countries_data': 
        #     {
        #         country : [
        #             {
        #                 'Country':country,
        #                 'Country_code_2':Country.objects.get(countryName=country).country_code_2,
        #                 'Year': entry['year'],
        #                 'Rank': entry['rank'],
        #                 'Amount': str(entry['amount'])
        #             }
        #             for entry in YearData.objects.filter(
        #                 rank__range = ranks,
        #                 country=country,
        #                 indicator=indicator_name
        #             ).values('year', 'rank', 'amount')
        #         ]
        #         for country in countries
        #     } 
        # }

        # queryset = YearData.objects.filter(indicator=indicator_name)
        # year_data_queryset = set(queryset.values_list('year'))
        # indica_years_list = [year[0] for year in year_data_queryset]

        # for country in data['countries_data']:
        #     country_data = data['countries_data'][country]
        #     years_with_data = {entry['Year'] for entry in country_data}
        #     missing_years = set(indica_years_list) - years_with_data
            
        #     for year in missing_years:
        #         country_data.append({
        #             'Country': country,
        #             'Country_code_2': Country.objects.get(countryName=country).country_code_2,
        #             'Year': year,
        #             'Rank': None,
        #             'Amount': None
        #         })
        #     data['countries_data'][country] = sorted(country_data, key=lambda entry: entry['Year'])

        # data['min_rank'] = min(rank_list,default="EMPTY")
        # data['max_rank'] = ranks[1]
        # data['min_amount'] = min(amount_list,default="EMPTY")
        # data['max_amount'] = max(amount_list,default="EMPTY")
        # data['year1'] = min(year_list,default="EMPTY")
        # data['year2'] = max(year_list,default="EMPTY")

        # if request!='' and request != def_request:
        #     return Response(result, status=status.HTTP_200_OK)
        # else:
        #     if def_request!='':
        #         return result
            



        # queryset = YearData.objects.filter(indicator=indicator_name)
        # result = {}
        
        # countries = country_name.split(',')
        # data = queryset.filter(country__in=countries)

        # result['countries_data'] = {
        #     entry['country']
        #     for entry in data
        #             .filter(rank__range = ranks)
        #             .values('country','year', 'rank', 'amount')
        # }

        # result['countries_data'] = {
        #         entry['country'] : [
        #             {
        #                 'Country':entry['country'],
        #                 'Country_code_2':Country.objects.get(countryName=entry['country']).country_code_2,
        #                 'Year': entry['year'],
        #                 'Rank': entry['rank'],
        #                 'Amount': str(entry['amount'])
        #             }
        #             for entry in data
        #             .filter(rank__range = ranks)
        #             .values('country','year', 'rank', 'amount')
        #             ]
        #         # for country in countries
        #     }

        # countries = country_name.split(',')
        # year_data = []
        # rank_list = []
        # amount_list = []
        # year_list = []
        # result = {}
        # print('start')
        # for country in countries:
        #     year_data.append(YearData.objects.filter(country = country, 
        #                                              indicator = indicator_name,)
        #                                              .values_list('rank','amount','year'))
        # print('finish')
        # for queryset in year_data:
        #     for value in queryset:
        #         rank_list.append(value[0])
        #         amount_list.append(value[1])
        #         year_list.append(value[2])
        
        # print('initialized')
        # result['countries_data'] = []

        # count= 0 
        # for entry in YearData.objects.filter(rank__range = ranks,country__in=countries,
        #                                      indicator=indicator_name).values('country','country_code','country_code_2','year', 'rank', 'amount'):
        #     count+=1
        #     print(count)


        # result = {'countries_data': 
        #     {
        #         count+=1 : [
        #             {
        #                 'Country':entry['country'],
        #                 'Country_code_2':Country.objects.get(countryName=country).country_code_2,
        #                 'Year': entry['year'],
        #                 'Rank': entry['rank'],
        #                 'Amount': str(entry['amount'])
        #             }
        #             for entry in YearData.objects.filter(
        #                 rank__range = ranks,
        #                 country__in=countries,
        #                 indicator=indicator_name
        #             ).values('year', 'rank', 'amount')
        #         ]
        #         # for country in countries
        #     } 
        # }
        
        # print('result initialized')

        # year_data_queryset = set(queryset.values_list('year'))
        # indica_years_list = [year[0] for year in year_data_queryset]

        # for country in result['countries_data']:
        #     country_data = result['countries_data'][country]
        #     years_with_data = {entry['Year'] for entry in country_data}
        #     missing_years = set(indica_years_list) - years_with_data
            
        #     for year in missing_years:
        #         country_data.append({
        #             'Country': country,
        #             'Country_code_2': Country.objects.get(countryName=country).country_code_2,
        #             'Year': year,
        #             'Rank': None,
        #             'Amount': None
        #         })
        #     result['countries_data'][country] = sorted(country_data, key=lambda entry: entry['Year'])

        # rank_list = []
        # amount_list = []
        # year_list = []

        # for _ in year_data:
        #     for value in _:
        #         print('entry',value)
        #         rank_list.append(value[0])
        #         amount_list.append(value[1])
        #         year_list.append(value[2])
        
        # result['min_rank'] = min(rank_list,default="EMPTY")
        # result['max_rank'] = max(rank_list,default="EMPTY")
        # result['min_amount'] = min(amount_list,default="EMPTY")
        # result['max_amount'] = max(amount_list,default="EMPTY")
        # result['year1'] = min(year_list,default="EMPTY")
        # result['year2'] = max(year_list,default="EMPTY")

        # return result
    