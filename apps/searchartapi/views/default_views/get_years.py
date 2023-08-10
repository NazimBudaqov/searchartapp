from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import MainData


class AvailableYearsView(APIView):
    # returns year for corresponding countries in given indicator
    def get(self, request):
        indicator_name = request.GET.get('indicator')
        country_name = str(request.GET.get('countries')).split(';')

        queryset = MainData.objects.select_related("indicator", "country").filter(
            indicator__indicatorName=indicator_name,
            country__countryName__in=country_name,
        )

        years = set()
        for data in queryset:
            for dict in data.json_data:
                # print(dict["year"])
                years.add(dict["year"])

        years = sorted(years)
        
        return Response(years)
