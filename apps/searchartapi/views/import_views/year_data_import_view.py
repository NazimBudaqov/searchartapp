from . import *

class MainDataImportViewClass(ViewSet):
    
    def post(self, csv_data):
        # Collecting data to be created
        ydata = csv_data[['Year', 'Rank', 'Amount', 'Country', 'Indicator']]
        print(f"length of data in csv file: {len(ydata)}")
        yd_objs = []

        # uploading main data
        row_limit = 510000
        batch_size = 10000
        start_row_count = YearData.objects.count()
        print('count: ',start_row_count)

        for batch_start in range(start_row_count, row_limit, batch_size):
            batch_end = min(batch_start + batch_size, row_limit)
            batch_data = ydata.iloc[batch_start:batch_end]

            for _, row in batch_data.iterrows():
                year, rank, amount, country, indicator = row
                if not YearData.objects.filter(year=year, country__countryName=country,indicator__indicatorName=indicator).exists():
                       
                    country_obj = Country.objects.get(countryName=country)
                    indica_obj = Indicator.objects.get(indicatorName=indicator)
                    year_data_obj = YearData(year=year, rank=rank, amount=amount,
                                            country=country_obj,
                                            indicator=indica_obj)
                    yd_objs.append(year_data_obj)

                    print(f"{_} data about country {country} at year {year} in indicator {indicator} uploaded")

            # Bulk create the objects for this batch
            YearData.objects.bulk_create(yd_objs)
            yd_objs = []  # Reset the list for the next batch

        print("Data upload complete.")


# class MainDataImportViewClass(ViewSet):
    
#     def post(self,csv_data):
#         # Collect data to be created
#         ydata = csv_data[['Year','Rank','Amount','Country','Indicator']]
#         print(f"length of data in csv file: {len(ydata)}")
#         yd_objs = []

#         # uploading main data
#         count_indica_ids = {'countries':[],'indicators':[]} #all
#         for db_country_row in Country.objects.all():
#             count_indica_ids['countries'].append({'id':db_country_row,'country':db_country_row.countryName})

#         for db_indica_row in Indicator.objects.all():
#             count_indica_ids['indicators'].append({'id':db_indica_row,'indica':db_indica_row.indicatorName})

#         row_limit = 510000
#         for _, row in ydata.iterrows():
#             if _ == row_limit:
#                 break
#             else:
#                 year,rank,amount,country,indicator = row
#                 if not YearData.objects.filter(year=year, country__countryName=country,
#                                             indicator__indicatorName=indicator
#                                             ).select_related('Country').exists():
#                     count_id = [country_id['id'] for country_id in 
#                                 count_indica_ids['countries']
#                                 if country_id['country'] == country
#                                 ][0]
#                     ind_id = [indica_id['id'] for indica_id in 
#                                 count_indica_ids['indicators'] 
#                                 if indica_id['indica'] == indicator
#                                 ][0]
#                     year_data_obj = YearData(year=year,rank=rank,amount=amount,
#                                             country=count_id,
#                                             indicator=ind_id)
#                     yd_objs.append(year_data_obj)
#                     print(f"{_} data about country {country} at year {year} in indicator {indicator} uploaded")

#         YearData.objects.bulk_create(yd_objs)
