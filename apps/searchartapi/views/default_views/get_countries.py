from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ...models import Country


class CountriesView(APIView):
    # returns countries and extreme ranks for given indicator and year
    def get(self, request, indicator_name):
        countries = []
        countries_data = (
            Country.objects.order_by("countryName")
            .filter(indicator__indicatorName=indicator_name)
            .distinct()
        )
        for country in countries_data:
            countries.append(country.countryName)

        data = {
            "countries": countries,
        }

        return Response(data, status=status.HTTP_200_OK)
