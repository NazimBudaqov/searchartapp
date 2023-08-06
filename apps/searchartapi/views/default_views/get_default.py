from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Prefetch
from django.core.exceptions import ObjectDoesNotExist

from ...models import Sector, Subsector 


class SectSubsectIndicaView(APIView):
    def get(self, request):
        try:
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
            try:
                data = {
                    "sectors": sectors,
                    "default_choices":[Sector.objects.get(sectorName='Economy').id,0,0]
                }
                return Response(data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response("there are no Sectors matching query.", status=status.HTTP_404_NOT_FOUND)
        
        except ObjectDoesNotExist:
            return Response("there are no Sectors matching query.", status=status.HTTP_404_NOT_FOUND)

