from . import *

class IndicatorCountryImportView(ViewSet):
    
    # assigning many-to-many relation between indicator and country tables
    #many-to-many fields data
    def many_to_many_assign(self,csv_data):
        indica_country_data = csv_data[['Indicator','Country']].drop_duplicates()

        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM searchartapi_indicator_countries")
            count_in_db = cursor.fetchone()[0]

        if len(indica_country_data) != count_in_db:
            ind_count_ids_check = 0

            for _, row in indica_country_data.iterrows():
                indicator_name = row['Indicator']
                country_name = row['Country']

                ind_ = Indicator.objects.get(indicatorName=indicator_name)
                count_id = Country.objects.get(countryName=country_name).id
                if ind_.countries.filter(id=count_id).exists():
                    # Relationship already exists, skip
                    pass
                else:
                    # Relationship does not exist, add it to table indicator_countries
                    query = f"INSERT INTO searchartapi_indicator_countries (indicator_id, country_id) VALUES ({ind_.id}, {count_id})"
                    with connection.cursor() as cursor:
                        cursor.execute(query)
                    print(f'ind {ind_.id} country {count_id}')
                ind_count_ids_check += 1
                print(f"relation checking {ind_count_ids_check}")
        else:
            print("Relations already assigned. Skipping...")
        #assign complete


    def post(self,csv_data):
        indicators = csv_data[['Indicator','Sector','Subsector']]
        indicators = indicators.drop_duplicates()

        countries = csv_data[['Country','Country_code','Country_code_2']]
        countries = countries.drop_duplicates()

        indica_objs = []
        country_objs = []

        for _, row in countries.iterrows():
            country_name = row['Country']
            country_code = row['Country_code']
            country_code_2 = row['Country_code_2']
            if not Country.objects.filter(countryName=country_name).exists():
                country_obj = Country(countryName=country_name, country_code=country_code,country_code_2=country_code_2)
                country_objs.append(country_obj)
                print(f"Country {country_name} created")
        Country.objects.bulk_create(country_objs)

        for _, row in indicators.iterrows():
            indicator_name = row['Indicator']
            sector_name = row['Sector']
            subsector_name = row['Subsector']
            if not Indicator.objects.filter(indicatorName=indicator_name,subsector__subSectorName=subsector_name).exists():
                subsec_obj = Subsector.objects.get(subSectorName=subsector_name,sector=Sector.objects.get(sectorName=sector_name))
                indica_obj = Indicator(indicatorName=indicator_name, subsector=subsec_obj)
                indica_objs.append(indica_obj)
                print(f"indicator {indicator_name} to subsector {subsector_name} created")
        Indicator.objects.bulk_create(indica_objs)

        self.many_to_many_assign(csv_data)
