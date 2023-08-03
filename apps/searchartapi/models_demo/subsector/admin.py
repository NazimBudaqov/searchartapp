from django.contrib import admin
from ..indicator.admin import IndicatorInline
from .model import Subsector

class SubsectorInline(admin.TabularInline):
    model = Subsector
    extra = 0

class SubsectorAdmin(admin.ModelAdmin):
    list_display = ['subSectorName','sector'] 
    readonly_fields = ['sector'] 
    ordering = ['subSectorName']
    inlines = [IndicatorInline]
admin.site.register(Subsector, SubsectorAdmin)