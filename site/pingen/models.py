from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class APICall(models.Model):

    # django.views.generic.base.View.http_method_names
    METHOD_CHOICES = (
        ('get', 'GET'),
        ('post', 'POST'),
        ('put', 'PUT'),
        ('patch', 'PATCH'),
        ('delete', 'DELETE'),
        ('head', 'HEAD'),
        ('trace', 'TRACE'),
        ('options', 'OPTIONS')
    )

    url = models.URLField(_('URL'), max_length=500)
    method = models.CharField(_('method'), max_length=10,
                              choices=METHOD_CHOICES)
    request_headers = models.TextField(_('request headers'), blank=True)
    request_data = models.TextField(_('request data'), blank=True)
    files = models.TextField(_('files'), blank=True)

    started_at = models.DateTimeField(_('Started at'), null=True, blank=True)
    ended_at = models.DateTimeField(_('Ended at'), null=True, blank=True)
    duration = models.DurationField(_('duration'), null=True, blank=True)

    status_code = models.PositiveSmallIntegerField(_('status_code'))
    response_headers = models.TextField(_('response headers'), blank=True)
    response_text = models.TextField(_('response text'), blank=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('API Call')
        verbose_name_plural = _('API Calls')
        ordering = ['-started_at']

    def __unicode__(self):  # pragma: no cover
        return u'{} {} {} {}'.format(
            self.started_at,
            self.get_method_display(),
            self.url,
            self.status_code
        )
