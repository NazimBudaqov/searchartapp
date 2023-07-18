from django.db import models

class Sector(models.Model):
    sectorName = models.CharField(max_length=100)
    def __str__(self):
        return self.sectorName
    
    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectors'

class Subsector(models.Model):
    subSectorName = models.CharField(max_length=100)
    sector = models.ForeignKey(Sector,related_name='subsectors',on_delete=models.CASCADE)
    def __str__(self):
        return self.subSectorName
    class Meta:
        verbose_name = 'Subsector'
        verbose_name_plural = 'Subsectors'

class Indicator(models.Model):
    indicatorName = models.CharField(max_length=160)
    subsector = models.ForeignKey(Subsector, on_delete=models.CASCADE)
    countries = models.ManyToManyField('Country')

    def __str__(self):
        return self.indicatorName
    class Meta:
        verbose_name = 'Indicator'
        verbose_name_plural = 'Indicators'

class Country(models.Model):
    countryName = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    country_code_2 = models.CharField(max_length=10)

    def __str__(self):
        return self.countryName
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

class YearData(models.Model):
    year = models.IntegerField()
    rank = models.IntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    indicator = models.ForeignKey(Indicator, on_delete=models.RESTRICT, null=False) #forbid deletion of indicator that easily

    def __str__(self):
        return str(self.year)
