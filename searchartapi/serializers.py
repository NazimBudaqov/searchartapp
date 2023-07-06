from rest_framework import serializers
from .models import Country,YearData,Sector,Subsector,Indicator

# dashboard data
class SectorSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['sectorName']
        
class IndicatorSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = ['indicatorName']

class YearDataSerialiazer(serializers.ModelSerializer):
        class Meta:
            model = YearData
            fields = ['year']

class CountrySerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['countryName']

# second api data
class DataSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_blank=True, max_length=255)
