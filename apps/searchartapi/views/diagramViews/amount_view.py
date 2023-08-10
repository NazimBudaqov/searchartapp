from django.forms import model_to_dict

from rest_framework.views import APIView
from ...models import MainData
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q


# diagram1 -  countries and their amount by selected ranks and year
class AmountView(APIView):
    def get(self="", request="", def_request=""):
        if request != "":
            pass
        else:
            if def_request != "":
                request = def_request
            else:
                return "false request"

        indicator_name = request.GET.get("indicator")
        countries = str(request.GET.get("countries")).split(";")
        year1 = int(request.GET.get("year1"))
        ranks = list(map(int, str(request.GET.get("ranks")).split(",")))

        queryset = MainData.objects.select_related("indicator").filter(
            indicator__indicatorName=indicator_name
        )
        result = {}

        amounts = []
        for data in queryset.filter(
            Q(json_data__year=year1) | Q(json_data__year__isnull=True)
        ):
            for item in data.json_data:
                if item["year"] == year1:
                    amounts.append(item["amount"])

        result["min_amount"] = min(amounts)
        result["max_amount"] = max(amounts)

        result["countries_by_rank"] = []
        for data in queryset.select_related("country").filter(
            country__countryName__in=countries
        ):
            for dict in data.json_data:
                if (dict["year"] == year1) and int(dict["rank"]) in range(
                    ranks[0], ranks[1] + 1
                ):
                    country_obj = model_to_dict(data.country)
                    result["countries_by_rank"].append(
                        {
                            "country": country_obj["countryName"],
                            "country_code": country_obj["country_code"],
                            "country_code_2": country_obj["country_code_2"],
                            "rank": dict["rank"],
                            "amount": dict["amount"],
                            "year": dict["year"],
                        }
                    )

        result["countries_by_rank"] = sorted(
            result["countries_by_rank"], key=lambda x: x["amount"], reverse=True
        )  # sort values by amount

        if request != "" and request != def_request:
            return Response(result, status=status.HTTP_200_OK)
        else:
            if def_request != "":
                return result
