
from django.core.management import BaseCommand
from django.utils.translation import ugettext_lazy as _

from djstripe.models import Invoice


class Command(BaseCommand):

    help = _('(Re)Generate PDF for invoice')

    def add_arguments(self, parser):  # pragma: no cover
        parser.add_argument('invoice_id', nargs='+', type=int)

        parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            dest='force',
            default=False,
            help=_('Override existing file(s)')
        )

    def handle(self, *args, **options):
        for pk in options.get('invoice_id', []):
            obj = Invoice.objects.filter(pk=pk).first()
            if obj is None:
                error_message = _(
                    'Could not find Invoice with id {}! Skipping...')
                self.stdout.write(error_message.format(pk))
                continue

            obj._generate_invoice_pdf(override_existing=options.get('force'))
