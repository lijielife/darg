
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
                subscriber = self.customer.subscriber  # company
                site = Site.objects.get_current()
                protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
                context = {
                    "charge": self,
                    "site": site,
                    "protocol": protocol,
                }

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

                if not subscriber.email or not subscriber.has_address:
                    # mail managers
                    subject = _('Company data missing')
                    context.update(dict(
                        email_missing=not subscriber.email,
                        address_missing=not subscriber.has_address
                    ))
                    message = render_to_string(
                        'djstripe/email/missing_company_data_body.txt',
                        context)
                    mail_managers(subject, message)
                    return

                # TODO: generate invoice pdf

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

                # TODO: attachment (pdf invoice)

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
