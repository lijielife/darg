
from functools import update_wrapper

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin, sites
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.html import mark_safe
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from reversion.admin import VersionAdmin

from shareholder.models import (Bank, Company, Country, Operator, OptionPlan,
                                OptionTransaction, Position, Security,
                                Shareholder, ShareholderStatement,
                                ShareholderStatementReport, UserProfile)


class ShareholderAdmin(VersionAdmin):

    list_display = ('get_full_name', 'company', 'number')
    search_fields = ['user__email', 'user__first_name', 'user__last_name',
                     'user__userprofile__company_name', 'number']
    list_filter = ('company',)

    def get_urls(self):

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        urls = [
            # FIXME: only when settings.DEBUG?
            url(r'^(.+)/statement_preview/$', wrap(self.statement_preview),
                name='shareholder_shareholder_statement_preview')
        ]
        return urls + super(ShareholderAdmin, self).get_urls()

    def statement_preview(self, request, object_id):
        obj = self.get_object(request, admin.utils.unquote(object_id))
        if not obj:
            raise Http404()
        context = dict(
            user=obj.user,
            user_name=obj.get_full_name(),
            company=obj.company,
            shareholder_list=[obj],
            report_date=now().date(),
            site=sites.models.Site.objects.get_current(),
            STATIC_URL=settings.STATIC_URL
        )
        return render_to_response(obj.company.statement_template.template.name,
                                  context, RequestContext(request))


class CompanyAdmin(VersionAdmin):

    def _operators(self, instance):
        markup = u'<a href="{url}">{text}</a>'
        admin_list_url = reverse('admin:shareholder_operator_changelist')
        operators = instance.operator_set.count()
        if not operators:
            return '-'
        text = operators == 1 and _('Operator') or _('Operators')
        context = dict(
            url=u'{}?company_id__exact={}'.format(admin_list_url, instance.pk),
            text=u'{} {}'.format(operators, text)
        )
        return markup.format(**context)
    _operators.short_description = _('Operators')
    _operators.allow_tags = True

    list_display = ('name', 'email', '_operators')
    search_fields = ('name', 'email')
    fieldsets = (
        ('', {'fields': ('name', 'founded_at', 'share_count',
                         'provisioned_capital', 'logo', 'pdf_header_image',
                         'email', 'vote_ratio', 'signatures')}),
        (_('Address'), {'fields': Company.ADDRESS_FIELDS}),
        (_('Statements'), {'fields': ('is_statement_sending_enabled',
                                      'send_shareholder_statement_via_letter_enabled',  # noqa
                                      'statement_sending_date')})
    )

    def get_urls(self):

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        urls = [
            # FIXME: only when settings.DEBUG?
            url(r'^(.+)/statement_preview/$', wrap(self.statement_preview),
                name='shareholder_company_statement_preview')
        ]
        return urls + super(CompanyAdmin, self).get_urls()

    def statement_preview(self, request, object_id):
        obj = self.get_object(request, admin.utils.unquote(object_id))
        if not obj:
            raise Http404()
        context = dict(
            user_name=_('Preview'),
            company=obj,
            report_date=now().date(),
            site=sites.models.Site.objects.get_current(),
            STATIC_URL=settings.STATIC_URL,
            preview=True
        )
        return render_to_response(obj.statement_template.template.name,
                                  context, RequestContext(request))


class BankAdmin(VersionAdmin):
    pass


class OperatorAdmin(VersionAdmin):
    list_display = ('id', 'user', 'company', 'date_joined')
    list_filter = ('company',)

    def date_joined(selfi, obj):
        return obj.user.date_joined


class PositionAdmin(VersionAdmin):
    list_display = (
        'bought_at', 'get_buyer', 'get_seller', 'count', 'value', 'get_company'
        )
    list_filter = ('buyer__company', 'seller__company', 'depot_type')
    search_fields = [
        'buyer__user__email', 'seller__user__email',
        'buyer__company__name', 'seller__company__name',
        'buyer__user__last_name', 'seller__user__last_name',
        'buyer__user__first_name', 'seller__user__first_name',
    ]

    def get_seller(self, obj):
        if obj.seller:
            return obj.seller.user.email
        return None

    def get_buyer(self, obj):
        if obj.buyer:
            return obj.buyer.user.email
        return None

    def get_company(self, obj):
        if obj.buyer:
            return obj.buyer.company
        elif obj.seller:
            return obj.seller.company
        return None


class UserProfileAdmin(VersionAdmin):

    list_display = ('user', 'full_name', 'street',
                    'street2', 'city')
    search_fields = [
        'user__first_name', 'user__email', 'user__last_name', 'user__username',
    ]

    def full_name(self, obj):
        return u'{} {}'.format(obj.user.first_name, obj.user.last_name)


class CountryAdmin(VersionAdmin):

    list_display = ('iso_code', 'name')
    search_fields = ['iso_code', 'name']


class SecurityAdmin(VersionAdmin):

    list_display = ('title', 'company', 'face_value')
    list_filter = ('company',)


class OptionTransactionAdmin(VersionAdmin):
    list_display = ('bought_at', 'buyer', 'seller',)


class OptionPlanAdmin(VersionAdmin):
    list_display = ('title', 'company')
    list_filter = ('company',)


class ShareholderStatementReportAdmin(admin.ModelAdmin):

    def _statements(self, instance):
        markup = u'<a href="{url}">{text}</a>'
        admin_list_url = reverse(
            'admin:shareholder_shareholderstatement_changelist')
        context = dict(
            url='{}?report_id__exact={}'.format(admin_list_url, instance.pk),
            text=u'{} {}'.format(
                instance.statement_count,
                ShareholderStatement._meta.verbose_name_plural)
        )
        return mark_safe(markup.format(**context))
    _statements.short_description = (
        ShareholderStatement._meta.verbose_name_plural)
    _statements.allow_tags = True

    list_display = ('company', 'report_date', '_statements')
    list_filter = ('report_date',)
    search_fields = ('company__name',)
    readonly_fields = ('statement_count', 'statement_sent_count',
                       'statement_opened_count', 'statement_downloaded_count',
                       'statement_letter_count', 'created_at', 'updated_at',
                       'pdf_file')
    fieldsets = (
        ('', {'fields': ('company', 'report_date', 'pdf_file')}),
        (_('shareholder statements'), {
            'fields': ('statement_count', 'statement_sent_count',
                       'statement_opened_count', 'statement_downloaded_count',
                       'statement_letter_count')
        }),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')})
    )


class TimestampListFilter(admin.SimpleListFilter):

    def lookups(self, request, model_admin):
        return (
            ('1', _('Yes')),
            ('0', _('No'))
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.exclude(**{self.field_name: None})
        elif self.value() == '0':
            return queryset.filter(**{self.field_name: None})
        return queryset


class EmailSentAtListFilter(TimestampListFilter):

    title = _('Was email sent')
    parameter_name = 'was_email_sent'
    field_name = 'email_sent_at'


class EmailOpenedAtListFilter(TimestampListFilter):

    title = _('Was email opened')
    parameter_name = 'was_email_opened'
    field_name = 'email_opened_at'


class PdfDownloadedAtListFilter(TimestampListFilter):

    title = _('Was PDF downloaded')
    parameter_name = 'was_pdf_downloaded'
    field_name = 'pdf_downloaded_at'


class LetterSentAtListFilter(TimestampListFilter):

    title = _('Was letter sent')
    parameter_name = 'was_letter_sent'
    field_name = 'letter_sent_at'


class ShareholderStatementAdmin(admin.ModelAdmin):

    def _user(self, instance):
        return instance.user.get_full_name() or instance.user.email
    _user.short_description = _('User')

    def _company(self, instance):
        return instance.report.company
    _company.short_description = _('company')

    def _report_date(self, instance):
        return instance.report.report_date
    _report_date.short_description = _('report date')

    def _email_sent(self, instance):
        markup = '<img src="{}admin/img/icon-{}.svg" alt="{}" />'
        return markup.format(settings.STATIC_URL,
                             instance.email_sent_at and 'yes' or 'no',
                             instance.email_sent_at and _('Yes') or _('No'))
    _email_sent.short_description = _('email sent')
    _email_sent.allow_tags = True

    def _email_opened(self, instance):
        markup = '<img src="{}admin/img/icon-{}.svg" alt="{}" />'
        return markup.format(settings.STATIC_URL,
                             instance.email_opened_at and 'yes' or 'no',
                             instance.email_opened_at and _('Yes') or _('No'))
    _email_opened.short_description = _('email opened')
    _email_opened.allow_tags = True

    def _pdf_downloaded(self, instance):
        markup = '<img src="{}admin/img/icon-{}.svg" alt="{}" />'
        return markup.format(settings.STATIC_URL,
                             instance.pdf_downloaded_at and 'yes' or 'no',
                             instance.pdf_downloaded_at and _('Yes') or _('No')
                             )
    _pdf_downloaded.short_description = _('pdf downloaded')
    _pdf_downloaded.allow_tags = True

    def _letter_sent(self, instance):
        markup = '<img src="{}admin/img/icon-{}.svg" alt="{}" />'
        return markup.format(settings.STATIC_URL,
                             instance.letter_sent_at and 'yes' or 'no',
                             instance.letter_sent_at and _('Yes') or _('No'))
    _letter_sent.short_description = _('letter sent')
    _letter_sent.allow_tags = True

    def _file_link(self, instance):
        if instance.pdf_file:
            return "<a href='%s'>download</a>" % (instance.pdf_download_url,)
        else:
            return "No PDF"
    _file_link.short_description = _('Download PDF')
    _file_link.allow_tags = True

    list_display = ('_user', '_company', '_report_date', '_email_sent',
                    '_email_opened', '_pdf_downloaded', '_letter_sent',
                    '_file_link')
    list_filter = ('report__report_date', EmailSentAtListFilter,
                   EmailOpenedAtListFilter, PdfDownloadedAtListFilter,
                   LetterSentAtListFilter)
    search_fields = ('user__username', 'user__first_name', 'user__last_name',
                     'report__company__name')
    readonly_fields = ('email_sent_at', 'email_opened_at', 'pdf_downloaded_at',
                       'letter_sent_at', 'pdf_file')


admin.site.register(Shareholder, ShareholderAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Security, SecurityAdmin)
admin.site.register(OptionPlan, OptionPlanAdmin)
admin.site.register(OptionTransaction, OptionTransactionAdmin)
admin.site.register(ShareholderStatementReport,
                    ShareholderStatementReportAdmin)
admin.site.register(ShareholderStatement, ShareholderStatementAdmin)
admin.site.register(Bank, BankAdmin)
