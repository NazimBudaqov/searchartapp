from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from . import *

class AllDiagramsView(APIView):
    def get(self,request,indicator_name,country_name): 
        year1 = int(request.GET.get('year1'))
        ranks = list(map(int,request.GET.get('ranks').split(',')))
        
        result = {
            "diagram_1":AmountView.get(year1,ranks,indicator_name,country_name),
            "diagram_2":RankDifferenceView.get(def_request=request,
                                                              indicator_name=indicator_name, 
                                                              country_name=country_name),
            "diagram_3_4":RankAmountDiagrams.get(ranks,indicator_name=indicator_name,
                                                                  country_name=country_name),
                }
        return Response(result,status=status.HTTP_200_OK)