from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        superuser = User.objects.create(
            email='admin@email.com',
            password='123',
            is_superuser=True,
            is_staff=True,
        )
        superuser.save()
