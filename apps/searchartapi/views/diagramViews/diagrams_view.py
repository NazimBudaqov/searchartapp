from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from django_filters.rest_framework import DjangoFilterBackend

from . import *

class AllDiagramsView(APIView):
    def get(self,request):
        result = {
            "diagram_1":AmountView.get(def_request=request),
            "diagram_2":RankDifferenceView.get(def_request=request),
            "diagram_3_4":RankAmountDiagrams.get(def_request=request),
                }
        return Response(result,status=status.HTTP_200_OK)

# class CountryDataListView(ListAPIView):
#     queryset = YearData.objects.all()
#     filterset_class = YearDataFilter
#     serializer_class = YearDataWithCountrySerializer
#     filter_backends = [DjangoFilterBackend]
