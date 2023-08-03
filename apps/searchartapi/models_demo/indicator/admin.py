from django.contrib import admin
from .model import Indicator

class IndicatorInline(admin.TabularInline):
    model = Indicator
    extra = 0
    fields = ['indicatorName']

class IndicatorAdmin(admin.ModelAdmin):
    list_display = ['indicatorName', 'subsector']
    exclude = ['countries']
    ordering = ['indicatorName']
admin.site.register(Indicator, IndicatorAdmin)