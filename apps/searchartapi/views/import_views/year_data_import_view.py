import json
import os
from . import *

class MainDataImportViewSet(ViewSet):

    def post(self,csv_data):
        # pass

        data_dict = {}
        for _,row in csv_data.iterrows():
            # if _ == 10000:
            #     break
            
            indicator_name = row['Indicator']
            country_name = row['Country']
            year = int(row['Year'])
            rank = int(row['Rank'])
            amount = float(row['Amount'])

            key = (indicator_name, country_name)
            if key not in data_dict:
                data_dict[key] = []

            data_dict[key].append({'year': year, 'rank': rank, 'amount': amount})

            print(f"{_}. Indicator: {indicator_name} country: {country_name} year: {year}")

        # Insert data into the MainData table using SQL INSERT
        with connection.cursor() as cursor:
            for (indicator_name, country_name), data in data_dict.items():
                # Get the IDs of the indicator and country using SQL SELECT
                cursor.execute('''
                    SELECT id FROM searchartapi_indicator WHERE indicatorName = %s
                ''', [indicator_name])
                indicator_id = cursor.fetchone()[0]

                cursor.execute('''
                    SELECT id FROM searchartapi_country WHERE countryName = %s
                ''', [country_name])
                country_id = cursor.fetchone()[0]

                # Create the JSON data for the group
                json_data = data

                # Insert data into the MainData table
                cursor.execute('''
                    INSERT INTO searchartapi_maindata (indicator_id, country_id, json_data)
                    VALUES (%s, %s, %s)
                ''', [indicator_id, country_id, json.dumps(json_data)])


        # with connection.cursor() as cursor:
        #     for _, row in csv_data.iterrows():
        #         indicator_name = row['Indicator']
        #         country_name = row['Country']
        #         year = int(row['Year'])
        #         rank = int(row['Rank'])
        #         amount = float(row['Amount'])

        #         # Get the IDs of the indicator and country using SQL SELECT
        #         cursor.execute('''
        #             SELECT id FROM searchartapi_indicator WHERE indicatorName = %s
        #         ''', [indicator_name])
        #         indicator_id = cursor.fetchone()[0]

        #         cursor.execute('''
        #             SELECT id FROM searchartapi_country WHERE countryName = %s
        #         ''', [country_name])
        #         country_id = cursor.fetchone()[0]

        #         # Insert data into the MainData table using SQL INSERT
        #         data = {
        #             "year": year,
        #             "rank": rank,
        #             "amount": amount,
        #         }
        #         cursor.execute('''
        #             INSERT INTO searchartapi_maindata (indicator_id, country_id, json_data)
        #             VALUES (%s, %s, %s)
        #         ''', [indicator_id, country_id, json.dumps(data)])

        #         print(f"{_}. Indicator: {indicator_name} country: {country_name} year: {year}")

        
        # Step 2: Use the connection.cursor() method to copy data from indicator_countries table
        # with connection.cursor() as cursor:
        #     cursor.execute('''
        #         INSERT INTO searchartapi_maindata (indicator_id, country_id)
        #         SELECT i.id, c.id
        #         FROM searchartapi_indicator i, searchartapi_country c
        #     ''')
        
        
        # with connection.cursor() as cursor:
        #     for row in csv_data:
        #         indicator = Indicator.objects.get(indicatorName=row['Indicator'])
        #         country = Country.objects.get(countryName=row['Country'])
        #         data = {
        #             "year": int(row['Year']),
        #             "rank": int(row['Rank']),
        #             "amount": float(row['Amount']),
        #         }
        #         cursor.execute('''
        #             UPDATE searchartapi_maindata
        #             SET json_data = %s
        #             WHERE indicator_id = %s AND country_id = %s
        #         ''', [json.dumps(data), indicator.id, country.id])

        # Step 3: Add JSON data to the json_data column
        # main_data_to_insert = []

        # count = 0
        # for index, row in csv_data.iterrows():
        #     indicator_name = row['Indicator']
        #     country_name = row['Country']
        #     year = row['Year']
        #     rank = row['Rank']
        #     amount = row['Amount']

        #     indicator = Indicator.objects.get(indicatorName=indicator_name)
        #     country = Country.objects.get(countryName=country_name)

        #     data = {
        #         "year": int(year),
        #         "rank": int(rank),
        #         "amount": float(amount),
        #     }

        #     main_data_to_insert.append(MainData(indicator=indicator, country=country, json_data=json.dumps(data)))

        #     # Bulk insert every 1000 rows to avoid memory issues
        #     if len(main_data_to_insert) >= 1000:
        #         MainData.objects.bulk_create(main_data_to_insert)
        #         main_data_to_insert = []
            
        #     count += 1
        #     print(f"{count}. Indicator: {indicator_name} country: {country_name} year: {year}")

        # # Insert the remaining data
        # MainData.objects.bulk_create(main_data_to_insert)


        

    '''
    def post(self,csv_data):
        
        # Collect data to be created
        ydata = csv_data[['Year', 'Rank', 'Amount', 'Country','Country_code', 'Country_code_2', 'Indicator']]
        print(f"csv: {csv_data} csv len = {len(csv_data)}")
        print(f"ydata: {ydata} ydata len = {len(ydata)}")

        # Save DataFrame to CSV file with only the necessary columns
        csv_file_path = 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/lastyears.csv'
        ydata.to_csv(csv_file_path, index=False, header=False)

        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM searchart.searchartapi_yeardata")
            count_in_db = cursor.fetchone()[0]
        print(f'rows count in MainData table {count_in_db}')

        with connection.cursor() as cursor:
            # SQL query to load data from the CSV file into the table
            if count_in_db < 1004537:
                print('starting loading file')

                sql = f"""
                    LOAD DATA INFILE '{csv_file_path}'
                    INTO TABLE searchart.searchartapi_maindata
                    FIELDS TERMINATED BY ','
                    OPTIONALLY ENCLOSED BY '"'
                    LINES TERMINATED BY '\\r\\n'
                    IGNORE 1 LINES
                    (`year`, `rank`, amount, country, country_code, country_code_2, indicator);
                """
                cursor.execute(sql)
                print("MainData upload complete.")

            else:
                print('data already in database'.upper())
                print('you must clean table before uploading same data again'.upper())


        # Delete the CSV file after the data import is complete
        os.remove(csv_file_path)
'''
    
    # def post(self, csv_data):
    #     # Collecting data to be created
    #     ydata = csv_data[['Year', 'Rank', 'Amount', 'Country', 'Indicator']]
    #     print(f"length of data in csv file: {len(ydata)}")
    #     yd_objs = []

    #     # uploading main data
    #     country_ids = {country.countryName: country for country in Country.objects.all()}
    #     indicator_ids = {indicator.indicatorName: indicator for indicator in Indicator.objects.all()}

    #     row_limit = 510000
    #     batch_size = 10000 #save every batch sized processed rows
    #     start_row_from_count = YearData.objects.count()
    #     print('data count in database: ', start_row_from_count)

    #     for batch_start in range(start_row_from_count, row_limit, batch_size):
    #         batch_end = min(batch_start + batch_size, row_limit)
    #         batch_data = ydata.iloc[batch_start:batch_end]

    #         for _, row in batch_data.iterrows():
    #             year, rank, amount, country, indicator = row
    #             if not YearData.objects.filter(year=year, country__countryName=country,indicator__indicatorName=indicator).exists():
                       
    #                 country_obj = country_ids.get(country)
    #                 indica_obj = indicator_ids.get(indicator)
    #                 year_data_obj = YearData(year=year, rank=rank, amount=amount,
    #                                         country=country_obj,
    #                                         indicator=indica_obj)
    #                 yd_objs.append(year_data_obj)

    #                 print(f"{_} data about country {country} at year {year} in indicator {indicator} uploaded")

    #         # Bulk create the objects for this batch
    #         YearData.objects.bulk_create(yd_objs)
    #         yd_objs = []  # Reset the list for the next batch

    #     print("Data upload complete.")


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
