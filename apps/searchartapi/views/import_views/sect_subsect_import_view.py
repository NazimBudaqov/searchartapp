from . import *

class SectSubsectImportViewClass(ViewSet):
    def post(self,csv_data):
        sectors = csv_data['Sector'].unique()
        subsectors = csv_data[['Subsector','Sector']]
        subsectors = subsectors.drop_duplicates()
        
        sector_objs = []
        subsec_objs = []

        for sector in sectors:
            if not Sector.objects.filter(sectorName=sector).exists():
                sector_obj = Sector(sectorName=sector)
                sector_objs.append(sector_obj)
                print(f"sector {sector} created")
        Sector.objects.bulk_create(sector_objs)
        
        for _, row in subsectors.iterrows():
            subsector_name = row['Subsector']
            sector_name = row['Sector']            
            if not Subsector.objects.filter(subSectorName=subsector_name).exists():
                sector_obj = Sector.objects.get(sectorName=sector_name)
                subsec_obj = Subsector(subSectorName=subsector_name, sector=sector_obj)
                subsec_objs.append(subsec_obj)
                print(f"subsector {subsector_name} with sector {sector_name} created")
        Subsector.objects.bulk_create(subsec_objs)
