from django.db import models

class Indicator(models.Model):
    indicatorName = models.CharField(max_length=160)
    subsector = models.ForeignKey(Subsector, on_delete=models.CASCADE)
    countries = models.ManyToManyField('Country')

    def __str__(self):
        return self.indicatorName
    class Meta:
        verbose_name = 'Indicator'
        verbose_name_plural = 'Indicators'
