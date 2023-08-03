from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView


from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend

from . import *
from ...models import Country, YearData
from ...serializers import CountrySerializer,YearDataSerializer,CountryIndicatorSerializer,YearDataWithCountrySerializer
from ...helpers import YearDataFilter

class AllDiagramsView(APIView):
    def get(self,request): 
        indicator_name = request.GET.get('indicator')
        country_names = str(request.GET.get('countries'))
        year1 = int(request.GET.get('year1'))
        ranks = list(map(int,str(request.GET.get('ranks')).split(',')))
        # print('request', indicator_name, country_names, year1, ranks)
        
        result = {
            "diagram_1":AmountView.get(def_request=request),
            "diagram_2":RankDifferenceView.get(def_request=request),
            "diagram_3_4":RankAmountDiagrams.get(def_request=request),
                }
        return Response(result,status=status.HTTP_200_OK)

# class CountryDataListView(ListAPIView):
#     queryset = YearData.objects.all()
#     filterset_class = YearDataFilter
#     serializer_class = YearDataWithCountrySerializer
#     filter_backends = [DjangoFilterBackend]

    # def get_amounts_diagram(self):
    #     data = YearData.objects.filter(draft=False).annotate(

    #     )
        
    #     serializer = YearDataSerializer(data=data)
    #     # print('request', request.query_params)
    #     if serializer.is_valid():
    #         print('serializer', serializer)
        
        
        # first diagram that illustrates countries and their amount by selected ranks, indicator name and then 
        # sorts it by ranks.
        # lst = []
        # countries_by_rank = []
        # result = {}
        # amount_list = []
        # year_list = []
            
        # try:
        #     year_data = YearData.objects.filter(country__in=countries, indicator=indicator_name, year=year)
        #     for data in year_data:
        #             country_obj = Country.objects.get(countryName=data.country)
        #             countries_by_rank.append({
        #                             'country': data.country,
        #                             'country_code': country_obj.country_code,
        #                             'country_code_2': country_obj.country_code_2,
        #                             'rank': data.rank,
        #                             'amount': data.amount,
        #                             'year':data.year
        #                 })
        #     lst.append(YearData.objects
        #                .filter(indicator = indicator_name,
        #                        year=year)
        #                .values_list('amount','year'))
        #     for queryset in lst:
        #         for value in queryset:
        #             amount_list.append(value[0])
        #             year_list.append(value[1])

        #     countries_by_rank = sorted(countries_by_rank, key=lambda x: x["amount"],reverse=True) #sort values by amount
        #     result['min_amount'] = min(amount_list,default="EMPTY")
        #     result['max_amount'] = max(amount_list,default="EMPTY")
        #     result['countries_by_rank'] = countries_by_rank

        #     return result

        # except ObjectDoesNotExist:
        #     return f"No {ObjectDoesNotExist.args} data found for the given criteria"
