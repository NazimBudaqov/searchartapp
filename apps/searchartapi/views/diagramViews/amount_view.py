from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from ...models import Country, YearData

#diagram1 -  countries and theri amount by selected ranks
class AmountView(APIView):
    def get(year, ranks, indicator_name, country_name):
        try:
            lst = []
            countries = country_name.split(',')
            countries_by_rank = []
            result = {}
            amount_list = []
            year_list = []
            
            for country_ in countries:
                year_data = YearData.objects.select_related('country','indicator').filter(country=Country.objects.get(countryName=country_), indicator__indicatorName=indicator_name, year=year, rank__range=ranks)
                for data in year_data:
                    countries_by_rank.append({
                                    'country': data.country.countryName,
                                    'country_code': data.country.country_code,
                                    'country_code_2': data.country.country_code_2,
                                    'rank': data.rank,
                                    'amount': data.amount,
                                    'year':data.year
                        })
            lst.append(YearData.objects
                       .filter(indicator__indicatorName = indicator_name,
                               year=year)
                       .values_list('amount','year'))
            for queryset in lst:
                for value in queryset:
                    amount_list.append(value[0])
                    year_list.append(value[1])
            countries_by_rank = sorted(countries_by_rank, key=lambda x: x["amount"],reverse=True) #sort values by amount
            result['min_amount'] = min(amount_list,default="EMPTY")
            result['max_amount'] = max(amount_list,default="EMPTY")
            result['countries_by_rank'] = countries_by_rank

            return result

        except ObjectDoesNotExist:
            return "No country or data found for the given criteria"
