
from django.apps import AppConfig
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, mail_managers
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

import stripe

from djstripe import settings as djstripe_settings

from utils.mail import is_valid_email


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
        self._tweak_djstripe_charge_send_receipt()

    def _tweak_djstripe_charge_send_receipt(self):

        # override receipt email sending to provide html email and attachment
        from django.contrib.sites.models import Site
        from djstripe.models import Charge

        def _send_receipt(self):
            if not self.receipt_sent:
                site = Site.objects.get_current()
                protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
                context = {
                    "charge": self,
                    "site": site,
                    "protocol": protocol,
                }

                # TODO: generate invoice pdf

                recipient = self._get_customer_email()

                if not recipient:
                    # mail managers
                    subject = _('Company email missing')
                    message = render_to_string(
                        'djstripe/email/missing_company_email_body.txt',
                        context)
                    mail_managers(subject, message)
                    return

                subject = render_to_string(
                    "djstripe/email/receipt_subject.txt", context)
                subject = subject.strip()
                text_content = render_to_string(
                    "djstripe/email/receipt_body.txt", context)

                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    to=[recipient],
                    from_email=djstripe_settings.INVOICE_FROM_EMAIL
                )

                # add html
                html_content = render_to_string(
                    "djstripe/email/receipt_body.html", context)
                email.attach_alternative(html_content, 'text/html')

                # TODO: attachment (pdf invoice)

                num_sent = email.send()
                self.receipt_sent = num_sent > 0
                self.save()

        Charge.send_receipt = _send_receipt

        # helper

        def _get_customer_email(self):
            email = self.customer.subscriber.email
            if not email:
                # fetch from stripe (this is just a worst case fallback)
                stripe.api_key = settings.STRIPE_SECRET_KEY
                customer = stripe.Customer.retrieve(
                    self.customer.stripe_id)
                email = (customer.get('email') or customer.get('name') or
                         customer.get('active_card', {}).get('name'))
                if is_valid_email(email):
                    self.customer.subscriber.email = email
                    self.customer.subscriber.save()
                else:
                    email = None

            return email

        Charge._get_customer_email = _get_customer_email
