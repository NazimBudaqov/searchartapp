from django.db import models

from .country import Country
from .indicator import Indicator

class MainData(models.Model):
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    json_data = models.JSONField(null=True, blank=True)

    
    class Meta:
        verbose_name = 'MainData'
        verbose_name_plural = 'MainData'
    
    def __str__(self):
        return str((self.country,self.indicator))