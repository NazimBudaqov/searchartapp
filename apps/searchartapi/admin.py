import re
from django.contrib import admin
from django.forms import inlineformset_factory
from .models import Country,Sector,Subsector,Indicator,YearData
from django.contrib.admin.models import LogEntry
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect

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

class YearDataInline(admin.TabularInline):
    model = YearData
    extra = 0
    verbose_name = 'Year data'
    verbose_name_plural = 'Each year data'
    ordering = ['indicator', 'year']
    readonly_fields = ('year','indicator')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        indicator_id = self.get_indicator_name(request)
        last_indicator_id = None
        if indicator_id:
            matches = re.findall(r'\d+', indicator_id)
            if matches:
                last_indicator_id = matches[-1]
        if last_indicator_id and last_indicator_id.isdigit():
            return qs.filter(indicator__indicatorName=Indicator.objects.get(id=int(last_indicator_id)))
    def get_indicator_name(self, request):
        return request.GET.get('_changelist_filters', None)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['countryName', 'country_code', 'country_code_2']
    inlines = [YearDataInline]
    list_filter = ['indicator']
    ordering = ['countryName']
