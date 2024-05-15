from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create an initial admin, if he does not exist yet'

    def handle(self, *args, **options):
        try:
            existing = User.objects.get(username= os.environ.get('ADMIN_USERNAME'))
        except User.DoesNotExist:
            existing = None
        if existing:
            print('Admin already exists')
            return
        user = User.objects.create_superuser(os.environ.get('ADMIN_USERNAME'), os.environ.get('ADMIN_EMAIL'), os.environ.get('ADMIN_PASSWORD'))
        user.save()
        self.stdout.write('Admin created')
