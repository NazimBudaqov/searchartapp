from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from . import amount_view, rank_difference_view, rank_amount_diagrams

class AllDiagramsView(APIView):
    def get(self,request,indicator_name,country_name): 
        year1 = int(request.GET.get('year1'))
        ranks = list(map(int,request.GET.get('ranks').split(',')))
            
        result = {
            "diagram_1":amount_view.AmountView.get(year1,ranks,indicator_name,country_name),
            "diagram_2":rank_difference_view.RankDifferenceView.get(def_request=request,
                                                              indicator_name=indicator_name, 
                                                              country_name=country_name),
            "diagram_3_4":rank_amount_diagrams.RankAmountDiagrams.get(ranks,indicator_name=indicator_name,
                                                                  country_name=country_name),
                }
        return Response(result,status=status.HTTP_200_OK)