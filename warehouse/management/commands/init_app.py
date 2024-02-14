import os
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    def handle(self, verbosity, *args, **options):
        from django.contrib.auth import get_user_model

        call_command('migrate')
        call_command('collectstatic', '--noinput')

        # create the default admin user
        User = get_user_model()
        try:
            User.objects.get(email='admin@example.com')
        except User.DoesNotExist:
            User.objects.create_superuser('admin@example.com', os.getenv('DEFAULT_ADMIN_PASSWORD', 'Platinum-2012'))
