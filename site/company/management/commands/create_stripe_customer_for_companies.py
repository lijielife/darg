
from django.conf import settings
from django.core.management import BaseCommand, CommandError

from shareholder.models import Company


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        if not settings.STRIPE_PUBLIC_KEY or not settings.STRIPE_SECRET_KEY:
            raise CommandError(
                'STRIPE_PUBLIC_KEY and STRIPE_SECRET_KEY required in settings')

        for company in Company.objects.all():
            company.get_customer()
