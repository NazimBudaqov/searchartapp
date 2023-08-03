from rest_framework import serializers
from ..models import YearData, Country

class YearDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearData
        fields = ('country', 'rank', 'amount', 'year')

class YearDataWithCountrySerializer(serializers.ModelSerializer):
    country_code = serializers.SerializerMethodField()
    country_code_2 = serializers.SerializerMethodField()

    class Meta:
        model = YearData
        fields = ['country','country_code', 'country_code_2', 'rank', 'amount', 'year', ]
    
    def get_country_code(self, obj):
        country_name = obj.country
        try:
            country = Country.objects.get(countryName=country_name)
            return country.country_code
        except Country.DoesNotExist:
            return None

    def get_country_code_2(self, obj):
        country_name = obj.country
        try:
            country = Country.objects.get(countryName=country_name)
            return country.country_code_2
        except Country.DoesNotExist:
            return None

# second api data
class DataSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_blank=True, max_length=255)
