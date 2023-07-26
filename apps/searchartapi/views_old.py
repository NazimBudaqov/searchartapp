import csv

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Min,Max
from django.db.models import Prefetch
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import viewsets,status

from .models import Sector, Subsector, Indicator, Country, YearData

'''
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)  
'''
'''
    default values:
        Sector: Economy
        Subsector: GDP and economic growth
        Indicator: Gross Domestic Product billions of U.S. dollars
        Country: All
        Year: 2019
        Rank: 1-10
'''
class ApiGetData(viewsets.ViewSet):
    #api - get dashboard data
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
    
    #after pressing Select button

    #diagram1 -  countries by selected ranks
    def get_diagram_1_data(self, year, ranks, indicator_name, country_name):
        try:
            lst = []
            countries = country_name.split(',')
            countries_by_rank = []
            result = {}
            amount_list = []
            year_list = []
            
            for country_ in countries:
                year_data = YearData.objects.filter(country=Country.objects.get(countryName=country_), indicator__indicatorName=indicator_name, year=year, rank__range=ranks)
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

    #diagram 2 - rank difference of countries by given indciator and years
    # can be accessed through both all_diagrams_data() requests and individual requests(to change diagram by selectable year1 and year2 values)
    def get_diagram_2_data(self, request='', def_request='', indicator_name='', country_name=''):
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

    # diagram 3 and 4 display country name,code and code_2 and change of their ranks and amounts  
    # data accordingly for chosen countries over all available years, by given indicator.  
    def get_diagram_3_4_data(self, ranks, indicator_name, country_name):
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

    # gets all diagrams data after select button
    # gets 'year1' and 'ranks' values from request
    def get_diagrams_data(self,request,indicator_name,country_name): 
        year1 = int(request.GET.get('year1'))
        ranks = list(map(int,request.GET.get('ranks').split(',')))
        
        result = {
            "diagram_1":self.get_diagram_1_data(year1,ranks,indicator_name,country_name),
            "diagram_2":self.get_diagram_2_data(def_request=request,indicator_name=indicator_name, 
                                                country_name=country_name),
            "diagram_3_4":self.get_diagram_3_4_data(ranks,indicator_name=indicator_name,
                                                    country_name=country_name),
                }
        return Response(result,status=status.HTTP_200_OK)
        
#import data from file(csv) to database
def import_data(request):
    if request.method == 'POST':
        file = request.FILES['file']
        reader = csv.DictReader(file.read().decode('utf-8').splitlines(), delimiter=';')
        count=1
        # 96,443 populated from 1,004,548
        target_row_number = 80559
        for i, row in enumerate(reader, start=1):
            if i < target_row_number:
                continue
            else:
                    # Extract data from each row using column names
                    sector_name = row['Sector']
                    subsector_name = row['Subsector']
                    indicator_name = row['Indicator']
                    country_name = row['Country']
                    country_code = row['Country_code']
                    country_code_2 = row['Country_code_2']
                    year = int(row['Year'])
                    rank = int(row['Rank'])
                    amount = float(row['Amount'].replace(',', ''))

                    # Create or get the related models
                    sector, _ = Sector.objects.get_or_create(sectorName=sector_name)
                    subsector, _ = Subsector.objects.get_or_create(subSectorName=subsector_name, sector=sector)
                    indicator, _ = Indicator.objects.get_or_create(indicatorName=indicator_name, subsector=subsector)
                    country, _ = Country.objects.get_or_create(countryName=country_name, country_code=country_code,
                                                               country_code_2=country_code_2)
                    year_data, _ = YearData.objects.get_or_create(year=year, rank=rank, amount=amount, country=country, 
                                                                  indicator = indicator)
                    # Assign relationships - only ManyToMany #ManyToOne-s are assigned in parenthesis
                    indicator.countries.add(country)
                    sector.save()
                    subsector.save()
                    indicator.save()
                    country.save()
                    year_data.save()
                    print(f"populated {count}")
                    count+=1
    return render(request, 'searchartapi/import.html')
