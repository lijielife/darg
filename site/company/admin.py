
from functools import update_wrapper

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin, messages
from django.core.management import call_command
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from djstripe.admin import (Charge, send_charge_receipt, Plan, Invoice,
                            customer_email, customer_has_card,
                            InvoiceItemInline,
                            InvoiceCustomerHasCardListFilter)


class ChargeAdmin(admin.ModelAdmin):

    readonly_fields = ('created',)
    list_display = [
        "stripe_id",
        "customer",
        "amount",
        "description",
        "paid",
        "disputed",
        "refunded",
        "fee",
        "receipt_sent",
        "created"
    ]
    search_fields = [
        "stripe_id",
        "customer__stripe_id",
        "card_last_4",
        "invoice__stripe_id"
    ]
    list_filter = [
        "paid",
        "disputed",
        "refunded",
        "card_kind",
        "created"
    ]
    raw_id_fields = [
        "customer",
        "invoice"
    ]
    actions = (send_charge_receipt,)


admin.site.unregister(Charge)
admin.site.register(Charge, ChargeAdmin)


class InvoiceAdmin(admin.ModelAdmin):

    def generate_pdf(self, request, queryset, force=False):  # pragma: no cover
        """
        generate PDF for invoice (calling management command)
        """
        pks = queryset.values_list('pk', flat=True)
        call_command('generate_invoice_pdf', ' '.join([str(pk) for pk in pks]),
                     force=force)
        message = _('Called management command "generate_invoice_pdf" for '
                    '{} object(s)').format(queryset.count())
        messages.info(request, message)

    generate_pdf.short_description = _('Generate PDF')

    def generate_pdf_forced(self, request, queryset):  # pragma: no cover
        """
        force (re)generation of invoice PDF (calling management command)
        """
        self.generate_pdf(request, queryset, force=True)

    generate_pdf_forced.short_description = _(
        'Generate PDF (override existing)')

    raw_id_fields = ('customer',)
    readonly_fields = ('created',)
    list_display = (
        "stripe_id",
        "paid",
        "closed",
        customer_email,
        customer_has_card,
        "period_start",
        "period_end",
        "subtotal",
        "total",
        "created"
    )
    search_fields = (
        "stripe_id",
        "customer__stripe_id"
    )
    list_filter = (
        InvoiceCustomerHasCardListFilter,
        "paid",
        "closed",
        "attempted",
        "attempts",
        "created",
        "date",
        "period_end",
        "total"
    )
    inlines = (InvoiceItemInline,)
    actions = (generate_pdf, generate_pdf_forced)

    # def get_urls(self):
    #
    #     def wrap(view):
    #         def wrapper(*args, **kwargs):
    #             return self.admin_site.admin_view(view)(*args, **kwargs)
    #         wrapper.model_admin = self
    #         return update_wrapper(wrapper, view)
    #
    #     urls = [
    #         # FIXME: only when settings.DEBUG?
    #         url(r'^(.+)/invoice_preview/$', wrap(self.invoice_preview),
    #             name='djstripe_charge_invoice_preview')
    #     ]
    #     return urls + super(InvoiceAdmin, self).get_urls()
    #
    # def invoice_preview(self, request, object_id):
    #     obj = self.get_object(request, admin.utils.unquote(object_id))
    #     if not obj:
    #         raise Http404()
    #
    #     context = obj._get_template_context()
    #     context.update(dict(
    #         from_address=settings.INVOICE_FROM_ADDRESS,
    #         from_email=settings.DEFAULT_FROM_EMAIL
    #     ))
    #
    #     template = obj.customer.subscriber.invoice_template
    #     return render_to_response(template, context, RequestContext(request))


admin.site.unregister(Invoice)
admin.site.register(Invoice, InvoiceAdmin)


# since we need to extra configuration for plans, we do this in settings
admin.site.unregister(Plan)
