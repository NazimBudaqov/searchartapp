import csv

from django.shortcuts import render

from ...models import Sector, Subsector, Indicator, Country, YearData

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
