from rest_framework import serializers
from ..models import Subsector

class SubsectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsector
        fields = ['subsectorName','sector']