from django.db import models
from django.contrib import admin
from .model import Sector
from ..subsector.admin import SubsectorInline

class SectorAdmin(admin.ModelAdmin):
    list_display = ['sectorName']
    inlines = [SubsectorInline]
admin.site.register(Sector, SectorAdmin)
