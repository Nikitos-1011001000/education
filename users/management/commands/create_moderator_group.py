from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Создаёт группу moderator, если её нет'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='moderator')
        if created:
            self.stdout.write('Группа moderator создана.')
        else:
            self.stdout.write('Группа moderator уже существует.')