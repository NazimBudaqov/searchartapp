from django.db import models

class Country(models.Model):
    countryName = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    country_code_2 = models.CharField(max_length=10)

    def __str__(self):
        return self.countryName
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
