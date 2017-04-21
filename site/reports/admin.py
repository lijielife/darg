from django.contrib import admin

from reports.models import Report


class ReportAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'user__first_name', 'user__last_name',
                     'company__name']
    list_filter = ('company', 'report_type', 'file_type')
    list_display = ('pk', 'company', 'report_type', 'file_type')


admin.site.register(Report, ReportAdmin)
