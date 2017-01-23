
from django.core.management import BaseCommand
from django.utils.translation import ugettext_lazy as _

from djstripe.models import Charge


class Command(BaseCommand):

    help = _('(Re)Generate PDF for invoice/charge')

    def add_arguments(self, parser):
        parser.add_argument('charge_id', nargs='+', type=int)

        parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            dest='force',
            default=False,
            help=_('Override existing file(s)')
        )

    def handle(self, *args, **options):
        for pk in options.get('charge_id'):
            obj = Charge.objects.filter(pk=pk).first()
            if obj is None:
                error_message = _(
                    'Could not find Charge with id {}! Skipping...').format(pk)
                self.stdout.write(error_message)
                continue

            obj._generate_invoice_pdf(override_existing=options.get('force'))
