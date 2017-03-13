from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.mail import mail_admins

User = get_user_model()


class Command(BaseCommand):
    help = ('Returns comma separated email list for newsletters and '
            'sends copy by mail')

    def handle(self, *args, **options):

        string = "\n".join([user.email for user in User.objects.filter(
                              operator__isnull=False).distinct()
                              ])
        self.stdout.write(string)
        self.stdout.write('- also sending as mail to admins...')
        mail_admins('full list of operator emails', string)
        self.stdout.write('finished')
