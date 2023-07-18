from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Min,Max

from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import Country, YearData

#diagram 2 - rank difference of countries by given indciator and years
# can be accessed through both all_diagrams_data() requests and individual 
# requests(to change diagram by selectable year1 and year2 values) 
class RankDifferenceView(APIView):
    def get(request='', def_request='', indicator_name='', country_name=''):
        #to use request variable only
        if request!='':
            pass
        else:
            if def_request!='':
                request=def_request
            else:
                return "false request"
        
        year1 = int(request.GET.get('year1'))
        if request.GET.get('year2'):
            year2 = int(request.GET.get('year2'))
        else:
            indicator_countries_year_list = YearData.objects.filter(indicator__indicatorName=indicator_name,country__countryName__in=country_name.split(',')).aggregate(min_year = Min("year"),max_year = Max('year'))
            year2 = indicator_countries_year_list['max_year']

        each_country_year_data = []

        for country in country_name.split(','):
            try :
                country_code = Country.objects.get(countryName = country).country_code
                country_code_2 = Country.objects.get(countryName = country).country_code_2
                country_id = Country.objects.get(countryName = country).id
                rank1 = YearData.objects.get(year = year1,
                                                country=country_id,
                                                indicator__indicatorName = indicator_name).rank
                amount1 = YearData.objects.get(year = year1,
                                                country=country_id,
                                                indicator__indicatorName = indicator_name).amount
                rank2 = YearData.objects.get(year = year2,
                                                country=country_id,
                                                indicator__indicatorName = indicator_name).rank
                amount2 = YearData.objects.get(year = year2,
                                                country=Country.objects.get(countryName = country),
                                                indicator__indicatorName = indicator_name).amount
                each_country_year_data.append(
                    {
                        'country':country,
                        'country_code':country_code,
                        'country_code_2':country_code_2,
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
            return Response(diagram2)
        else:
            if def_request!='':
                return diagram2