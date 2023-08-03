import re
from django.contrib import admin
from ..yeardata.model import YearData
from ..indicator.model import Indicator
from .model import Country

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
    # inlines = [YearDataInline]
    list_filter = ['indicator']
    ordering = ['countryName']