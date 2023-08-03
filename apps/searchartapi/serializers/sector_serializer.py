from rest_framework import serializers
from ..models import Sector

# dashboard data
class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['sectorName']