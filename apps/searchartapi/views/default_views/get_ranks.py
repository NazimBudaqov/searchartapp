from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ...models import MainData

class AvailableRanksView(APIView):
    def get(self, request):
        indicator_name = request.GET.get('indicator')
        year = request.GET.get('year')

        queryset = MainData.objects.select_related("indicator").filter(
            indicator__indicatorName=indicator_name,
        )

        # get min and max rank
        ranks_list = []
        for data in queryset:
            for item in data.json_data:
                if item['year'] == int(year):
                    ranks_list.append(item["rank"])
        
        result = {
            "min_rank": min(ranks_list, default="EMPTY"),
            "max_rank": max(ranks_list, default="EMPTY"),
        }

        return Response(result, status=status.HTTP_200_OK)
