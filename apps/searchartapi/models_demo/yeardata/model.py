from django.db import models
from ..country.model import Country
from ..indicator.model import Indicator

class YearData(models.Model):
    year = models.IntegerField()
    rank = models.IntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    indicator = models.ForeignKey(Indicator, on_delete=models.RESTRICT, null=False) #forbid deletion of indicator that easily

    def __str__(self):
        return str(self.year)