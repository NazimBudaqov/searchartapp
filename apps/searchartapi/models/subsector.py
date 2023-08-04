from django.db import models

from .sector import Sector

class Subsector(models.Model):
    subSectorName = models.CharField(max_length=100)
    sector = models.ForeignKey(Sector,related_name='subsectors',on_delete=models.CASCADE)
    def __str__(self):
        return self.subSectorName
    class Meta:
        verbose_name = 'Subsector'
        verbose_name_plural = 'Subsectors'