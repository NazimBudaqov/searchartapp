from ...models import Country, YearData
from rest_framework.views import APIView
# diagram 3 and 4 display country name,code and code_2 and change of their ranks and amounts  
# data accordingly for chosen countries over all available years, by given indicator.
class RankAmountDiagrams(APIView):
    def get(ranks, indicator_name, country_name):
        countries = country_name.split(',')
        year_data = []
        rank_list = []
        amount_list = []
        year_list = []

        for country in countries:
            year_data.append(YearData.objects.filter(country__countryName = country, 
                                                     indicator__indicatorName = indicator_name,
                                                     year__in=YearData.objects.filter(country__countryName = country, 
                                                                                      indicator__indicatorName = indicator_name)
                                                                                      .values_list('year'))
                                                                                      .values_list('rank','amount','year'))
        for queryset in year_data:
            for value in queryset:
                rank_list.append(value[0])
                amount_list.append(value[1])
                year_list.append(value[2])
        
        data = {'countries_data': 
            {
                country : [
                    {
                        'Country':country,
                        'Country_code_2':Country.objects.get(countryName=country).country_code_2,
                        'Year': entry['year'],
                        'Rank': entry['rank'],
                        'Amount': str(entry['amount'])
                    }
                    for entry in YearData.objects.filter(
                        rank__range = ranks,
                        country__countryName=country,
                        indicator__indicatorName=indicator_name
                    ).values('year', 'rank', 'amount')
                ]
                for country in countries
            } 
        }

        data['min_rank'] = min(rank_list,default="EMPTY")
        data['max_rank'] = ranks[1]
        data['min_amount'] = min(amount_list,default="EMPTY")
        data['max_amount'] = max(amount_list,default="EMPTY")
        data['year1'] = min(year_list,default="EMPTY")
        data['year2'] = max(year_list,default="EMPTY")

        return data