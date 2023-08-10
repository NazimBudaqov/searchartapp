import re

import json
import logging

from .models import MainData, Sector, Subsector, Indicator, Country

from django.contrib import admin
from django.db.models import JSONField 
from django.forms import widgets

class SubsectorInline(admin.TabularInline):
    model = Subsector
    extra = 0
class SectorAdmin(admin.ModelAdmin):
    list_display = ['sectorName']
    inlines = [SubsectorInline]
admin.site.register(Sector, SectorAdmin)

class IndicatorInline(admin.TabularInline):
    model = Indicator
    extra = 0
    fields = ['indicatorName']
class SubsectorAdmin(admin.ModelAdmin):
    list_display = ['subSectorName','sector'] 
    readonly_fields = ['sector'] 
    ordering = ['subSectorName']
    inlines = [IndicatorInline]
admin.site.register(Subsector, SubsectorAdmin)

class IndicatorAdmin(admin.ModelAdmin):
    list_display = ['indicatorName', 'subsector']
    exclude = ['countries']
    ordering = ['indicatorName']
admin.site.register(Indicator, IndicatorAdmin)

# class MainDataInline(admin.TabularInline):
#     model = MainData
#     extra = 0
#     verbose_name = 'Main data'
#     verbose_name_plural = 'Each year data'
#     ordering = ['indicator', 'country']
#     readonly_fields = ('json_data','indicator')

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         indicator_id = self.get_indicator_name(request)
#         last_indicator_id = None
#         if indicator_id:
#             matches = re.findall(r'\d+', indicator_id)
#             if matches:
#                 last_indicator_id = matches[-1]
#         if last_indicator_id and last_indicator_id.isdigit():
#             return qs.filter(indicator__indicatorName=Indicator.objects.get(id=int(last_indicator_id)))
    
#     def get_indicator_name(self, request):
#         return request.GET.get('_changelist_filters', None)

logger = logging.getLogger(__name__)


class PrettyJSONWidget(widgets.Textarea):

    def format_value(self, value):
        try:
            value = json.dumps(json.loads(value), indent=2, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in value.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception as e:
            logger.warning("Error while formatting JSON: {}".format(e))
            return super(PrettyJSONWidget, self).format_value(value)


class MainDataAdmin(admin.ModelAdmin):
    list_display = ["country",'indicator']
    list_filter = ['indicator']
    ordering = ['indicator','country']
    readonly_fields = ('indicator','json_data')
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }

admin.site.register(MainData, MainDataAdmin)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['countryName', 'country_code', 'country_code_2']
    # inlines = [MainDataInline]
    ordering = ['countryName']
