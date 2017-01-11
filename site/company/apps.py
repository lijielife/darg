
from django.apps import AppConfig
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


class CompanyAppConfig(AppConfig):

    name = 'company'
    verbose_name = _("Company")

    def ready(self):
        super(CompanyAppConfig, self).ready()

        # load stripe event handlers
        from . import event_handlers  # NOQA

        # override receipt email sending to provide html email and attachment
        from django.contrib.sites.models import Site
        from django.core.mail import EmailMultiAlternatives
        from djstripe import settings as djstripe_settings
        from djstripe.models import Charge

        def _send_receipt(self):
            if not self.receipt_sent:
                site = Site.objects.get_current()
                protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
                ctx = {
                    "charge": self,
                    "site": site,
                    "protocol": protocol,
                }
                subject = render_to_string(
                    "djstripe/email/receipt_subject.txt", ctx)
                subject = subject.strip()
                text_content = render_to_string(
                    "djstripe/email/receipt_body.txt", ctx)
                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    to=[self.customer.subscriber.email],
                    from_email=djstripe_settings.INVOICE_FROM_EMAIL
                )

                # add html
                html_content = render_to_string(
                    "djstripe/email/receipt_body.html", ctx)
                email.attach_alternative(html_content, 'text/html')

                # TODO: attachment? (pdf invoice)

                num_sent = email.send()
                self.receipt_sent = num_sent > 0
                self.save()

        Charge.send_receipt = _send_receipt
