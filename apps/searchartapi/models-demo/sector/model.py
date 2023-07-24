from django.db import models


class Sector(models.Model):
    sectorName = models.CharField(max_length=100)
    def __str__(self):
        return self.sectorName
    
    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectors'
