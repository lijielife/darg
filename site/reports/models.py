from __future__ import unicode_literals

import datetime
import os

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from project.models import TimeStampedModel
from shareholder.models import Company

REPORT_FILE_TYPES = (
    ('PDF', 'PDF'),
    ('XLS', 'XLS'),
)

REPORT_TYPES = (
    ('captable', _('Active Shareholders')),
    ('assembly_participation', _('Assembly Participation')),
)

ORDERING_TYPES = (
    ('user__last_name', _('Last Name')),
    ('user__last_name_desc', _('Last Name (descending)')),
    ('get_full_name', _('Last Name')),
    ('get_full_name_desc', _('Last Name (descending)')),
    ('share_count', _('Share Count')),
    ('share_count_desc', _('Share Count (descending)')),
    ('number', _('Shareholder Number')),
    ('number_desc', _('Shareholder Number (descending)')),
    ('share_percent', _('Share Percent Ownership')),
    ('share_percent_desc', _('Share Percent Ownership (descending)')),
    ('cumulated_face_value', _('face value total capital')),
    ('cumulated_face_value_desc', _('face value total capital (descending)')),
    ('user__userprofile__postal_code', _('postal code')),
    ('user__userprofile__postal_code_desc', _('postal code (descending)')),
)


def get_report_upload_path(instance, filename):
    return os.path.join(
        "private", "reports", "%s" % instance.company.pk,
        "%d" % instance.id, filename)


class Report(TimeStampedModel):
    """
    each single generated file as a report
    """
    company = models.ForeignKey(Company)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    file_type = models.CharField(choices=REPORT_FILE_TYPES, max_length=3)
    report_type = models.CharField(choices=REPORT_TYPES, max_length=100)
    # cannot be named ordering due to DRF ordering filter
    order_by = models.CharField(choices=ORDERING_TYPES, max_length=255)
    file = models.FileField(
        upload_to=get_report_upload_path, null=True, blank=True)
    eta = models.DateTimeField(_('Estimated rendering completion time'))
    generated_at = models.DateTimeField(_('file creation datetime'), null=True,
                                        blank=True)
    generation_time = models.PositiveIntegerField(
        _('time it took to generate the file in seconds'),
        null=True, blank=True)
    report_at = models.DateField(_('report filter date'))
    downloaded_at = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return u"{}_{}_{}.{}".format(self.created_at, self.company.name,
                                     self.report_type, self.file_type.lower())

    def get_absolute_url(self):
        return reverse('reports:download', kwargs={'report_id': self.pk})

    def get_filename(self):
        if self.file_type == 'XLS':
            file_type = 'xlsx'
        else:
            file_type = self.file_type.lower()
        return u"report-{}-{}-{}.{}".format(slugify(self.company), self.pk,
                                            self.report_type, file_type)

    def render(self, notify=False, track_downloads=False):
        """ trigger the right task to render the file """
        # avoid circular import
        from reports.tasks import (render_captable_pdf,
                                   render_captable_xls,
                                   render_assembly_participation_xls)

        args = [self.company.pk, self.pk]
        kwargs = {'ordering': self.order_by, 'notify': notify,
                  'track_downloads': track_downloads}
        if self.user:
            kwargs.update({'user_id': self.user.pk})

        # FIXME build render method name dynamically and remove ifs
        if self.report_type == 'captable':
            if self.file_type == 'PDF':
                render_captable_pdf.apply_async(args=args, kwargs=kwargs)
            elif self.file_type == 'XLS':
                render_captable_xls.apply_async(args=args, kwargs=kwargs)

        elif self.report_type == 'assembly_participation':
            render_assembly_participation_xls.apply_async(
                args=args, kwargs=kwargs)
            # elif self.file_type == 'PDF':
            #    render_captable_pdf.apply_async(args=args, kwargs=kwargs)

        else:
            raise NotImplementedError('report cannot be created')

    def update_eta(self):
        """ get from last item of same type or default 3m from now """
        # use last reports generation time for estimate or use default of X
        # minutes
        prev_report = Report.objects.filter(
            file_type=self.file_type,
            order_by=self.order_by,
            report_type=self.report_type,
            company=self.company,
            ).order_by('-pk')
        if self.pk:
            prev_report = prev_report.exclude(pk=self.pk)
        prev_report = prev_report.first()
        seconds = getattr(prev_report, 'generation_time', None) or 3*60

        self.eta = timezone.now() + datetime.timedelta(seconds=seconds)
        self.save()
