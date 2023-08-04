from django.db import models

class YearData(models.Model):
    year = models.IntegerField()
    rank = models.IntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=3, blank=True, null=True)
    country_code_2 = models.CharField(max_length=2, blank=True, null=True)
    indicator = models.CharField(max_length=160)
    
    def __str__(self):
        return str(self.year)