from django.contrib import admin

from .models import InvestigateUrlModel, PhishVerdictModel, UserLicenseVerdictMap, OffloadTasksModel


class InvestigateUrlModelAdmin(admin.ModelAdmin):
    list_display = ('analysis_url', )
    list_filter = ['analysis_url']
    search_fields = ['analysis_url']
    fieldsets = [
        (None,               {'fields': ['analysis_url']}),
        ('Date information', {'fields': ['created_date', 'modified_date'], 'classes': ['collapse']}),
    ]

class PhishVerdictModelAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'analysis_stage_text', 'internal_download_path', )


#admin.site.register(InvestigateUrlModel)
admin.site.register(InvestigateUrlModel, InvestigateUrlModelAdmin)

#admin.site.register(PhishVerdictModel)
admin.site.register(PhishVerdictModel, PhishVerdictModelAdmin)

admin.site.register(UserLicenseVerdictMap)

class OffloadTasksModelAdmin(admin.ModelAdmin):
    list_display = ('phish_verdict_model', 'time_sha', 'created_date', 'modified_date')

admin.site.register(OffloadTasksModel, OffloadTasksModelAdmin)
