from rest_framework import serializers
from ..models import Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['countryName','country_code','country_code_2']

class CountryIndicatorSerializer(serializers.Serializer):
    countries = serializers.ListField(child=serializers.CharField())
    indicator = serializers.CharField()

class CountryYearDataSerializer(serializers.Serializer):
    countries = serializers.ListField(child=serializers.CharField())
    ranks = serializers.CharField()
    year = serializers.CharField()
