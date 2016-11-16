
from django.contrib import admin
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _

from .models import APICall


class APICallAdmin(admin.ModelAdmin):

    def _url(self, instance):
        return Truncator(instance.url).chars(100)
    _url.short_description = _('URL')

    list_display = ('_url', 'method', 'status_code', 'started_at')
    list_filter = ('started_at', 'method', 'status_code')
    readonly_fields = ('url', 'method', 'request_headers', 'request_data',
                       'files', 'started_at', 'ended_at', 'duration',
                       'status_code', 'response_headers', 'response_text',
                       'created_at', 'updated_at')
    fieldsets = (
        (_('request'), {'fields': ('url', 'method', 'request_headers',
                                   'request_data', 'files')}),
        (_('Timestamps'), {'fields': (('started_at', 'ended_at', 'duration'),
                                      ('created_at', 'updated_at'))}),
        (_('response'), {'fields': ('status_code', 'response_headers',
                                    'response_text')})
    )

    def has_add_permission(self, request):
        return False

admin.site.register(APICall, APICallAdmin)
