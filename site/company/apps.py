
import logging
import os

from django.apps import AppConfig
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.utils.translation import (ugettext_lazy as _,
                                      activate as activate_lang)

import stripe

from djstripe import settings as djstripe_settings

from utils.mail import is_valid_email
from utils.pdf import render_pdf


# logger = logging.getLogger(__name__)
logger = logging.getLogger('celery')


class CompanyAppConfig(AppConfig):

    name = 'company'
    verbose_name = _("Company")

    def ready(self):
        super(CompanyAppConfig, self).ready()

        # load stripe event handlers
        from . import event_handlers  # NOQA

        # load signals
        from . import signals  # NOQA

        # overwrite 3rd party app model method
        self._tweak_djstripe_charge()
        self._tweak_djstripe_invoice()

    def _tweak_djstripe_charge(self):
        """
        override receipt email sending to provide html email and attachment
        """

        from django.contrib.sites.models import Site
        from djstripe.models import Charge

        def _send_receipt(self):
            if not self.receipt_sent:
                subscriber = self.customer.subscriber  # company
                context = self._get_template_context()
                recipient = subscriber.email
                has_address = subscriber.has_address

                if not recipient or not has_address:
                    data = self._get_customer_data()

                if not recipient:
                    # get email address from stripe data
                    recipient = (data.get('email') or data.get('name') or
                                 data.get('active_card', {}).get('name'))
                    if is_valid_email(recipient):
                        subscriber.email = recipient
                        subscriber.save()

                if not has_address:
                    # get postal address from stripe data
                    active_card = data.get('active_card', {})
                    subscriber.read_address_from_stripe_object(active_card)

                if not subscriber.email:
                    error_message = _(
                        'Company "{}" (ID {}) was charged but has no email '
                        'address stored').format(subscriber, subscriber.pk)
                    logger.exception(error_message)
                    return

                if not subscriber.has_address:
                    error_message = _(
                        'Company "{}" (ID {}) was charged but has no postal '
                        'address stored').format(subscriber, subscriber.pk)
                    logger.exception(error_message)

                # generate invoice pdf
                if self.invoice:
                    pdf_invoice = self.invoice._generate_invoice_pdf(
                        override_existing=True)
                else:
                    pdf_invoice = None

                include_invoice_items = getattr(
                    settings, 'COMPANY_INVOICE_INCLUDE_IN_EMAIL', None)
                if include_invoice_items is None:
                    include_invoice_items = not bool(pdf_invoice)
                invoice_items = (
                    include_invoice_items and context['invoice_items'] or [])
                context.update(dict(invoice_items=invoice_items))

                subject = render_to_string(
                    "djstripe/email/receipt_subject.txt", context)
                subject = subject.strip()
                text_content = render_to_string(
                    "djstripe/email/receipt_body.txt", context)

                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    to=[subscriber.email],
                    from_email=djstripe_settings.INVOICE_FROM_EMAIL
                )

                # add html
                html_content = render_to_string(
                    "djstripe/email/receipt_body.html", context)
                email.attach_alternative(html_content, 'text/html')

                # attachment (pdf invoice)
                if pdf_invoice:
                    with open(pdf_invoice, 'r') as f:
                        invoice_content = f.read()
                    filename = os.path.basename(pdf_invoice)
                    email.attach(filename, invoice_content, 'application/pdf')

                num_sent = email.send()
                self.receipt_sent = num_sent > 0
                self.save()

        Charge.send_receipt = _send_receipt

        # helper

        def _get_customer_data(self):
            """
            fetch customer from stripe api
            """
            stripe.api_key = settings.STRIPE_SECRET_KEY
            try:
                return stripe.Customer.retrieve(self.customer.stripe_id)
            except:
                pass

            return dict()

        Charge._get_customer_data = _get_customer_data

        def _get_template_context(self):
            """
            get context for templates (email)
            """
            if self.invoice:
                invoice_items = self.invoice.items.all().order_by(
                    '-line_type', '-period_start')
            else:
                invoice_items = []

            context = dict(
                charge=self,
                # invoice=self.invoice,
                invoice_items=invoice_items,
                company=self.customer.subscriber,
                site=Site.objects.get_current(),
                STATIC_URL=settings.STATIC_URL,
                include_vat=settings.COMPANY_INVOICE_INCLUDE_VAT,
                plan=settings.DJSTRIPE_PLANS.get(
                    self.customer.current_subscription.plan, {}),
                protocol=settings.DEFAULT_HTTP_PROTOCOL
            )

            if context['include_vat']:
                net = self.amount / (100 + settings.COMPANY_INVOICE_VAT) * 100
                vat_value = self.amount - net
                context.update(dict(
                    vat=settings.COMPANY_INVOICE_VAT,
                    vat_value=vat_value
                ))

            return context

        Charge._get_template_context = _get_template_context

    def _tweak_djstripe_invoice(self):
        """
        add pdf invoice handling
        """

        from django.contrib.sites.models import Site
        from djstripe.models import Invoice

        def _generate_invoice_pdf(self, override_existing=False):
            """
            create a PDF invoice for charge
            if `override_existing` is True (default: False) - regenerate PDF
            """

            if not self.customer.subscriber.has_address:
                error_message = _(
                    'Company "{}" (ID {}) was charged but has no postal '
                    'address stored').format(self.customer.subscriber,
                                             self.customer.pk)
                logger.exception(error_message)

            context = self._get_template_context()
            context.update(dict(
                from_address=settings.INVOICE_FROM_ADDRESS,
                from_email=settings.DEFAULT_FROM_EMAIL
            ))

            pdf_filepath = self._get_pdf_filepath()

            # check if exists
            if os.path.exists(pdf_filepath) and not override_existing:
                return pdf_filepath

            activate_lang(settings.LANGUAGE_CODE)
            template = get_template(self.customer.subscriber.invoice_template)
            pdf = render_pdf(template.render(context))

            if not pdf:
                error_message = _(
                    'Company "{}" (ID {}) was charged but invoice pdf could'
                    ' not be generated.').format(self.customer.subscriber,
                                                 self.customer.subscriber.pk)
                logger.exception(error_message)
                return None

            with open(pdf_filepath, 'w') as f:
                f.write(pdf.getvalue())

            return pdf_filepath

        Invoice._generate_invoice_pdf = _generate_invoice_pdf

        def _get_invoice_pdf_path_for_company(self, company):
            """
            returns a unique directory path to for the charge
            """
            path = os.path.join(settings.COMPANY_INVOICES_ROOT,
                                str(company.pk),
                                str(self.pk))
            if not os.path.exists(path):
                os.makedirs(path)
            return path

        Invoice._get_invoice_pdf_path_for_company = (
            _get_invoice_pdf_path_for_company)

        def _get_pdf_filepath(self):
            """
            return complete filepath to PDF
            """
            pdf_dir = self._get_invoice_pdf_path_for_company(
                self.customer.subscriber)
            pdf_filename = u'{}-{}.pdf'.format(
                settings.COMPANY_INVOICE_FILENAME, self.pk)
            return os.path.join(pdf_dir, pdf_filename)

        Invoice._get_pdf_filepath = _get_pdf_filepath

        def _has_invoice_pdf(self):
            """
            return boolean whether invoice PDF exists or not
            """
            filepath = self._get_pdf_filepath()
            return os.path.exists(filepath) and os.path.isfile(filepath)

        Invoice.has_invoice_pdf = property(_has_invoice_pdf)

        def _get_template_context(self):
            """
            get context for template (pdf)
            """

            invoice_items = self.items.all().order_by(
                '-line_type', '-period_start')

            context = dict(
                # charge=self,
                invoice=self,
                invoice_items=invoice_items,
                company=self.customer.subscriber,
                site=Site.objects.get_current(),
                STATIC_URL=settings.STATIC_URL,
                include_vat=settings.COMPANY_INVOICE_INCLUDE_VAT,
                plan=settings.DJSTRIPE_PLANS.get(
                    self.customer.current_subscription.plan, {}),
                protocol=settings.DEFAULT_HTTP_PROTOCOL
            )

            if context['include_vat']:
                net = self.total / (100 + settings.COMPANY_INVOICE_VAT) * 100
                vat_value = self.total - net
                context.update(dict(
                    vat=settings.COMPANY_INVOICE_VAT,
                    vat_value=vat_value
                ))

            return context

        Invoice._get_template_context = _get_template_context
