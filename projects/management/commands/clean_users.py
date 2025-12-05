from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Role

class Command(BaseCommand):
    help = "Cleans users and resets to default admin and test users"

    def handle(self, *args, **kwargs):
        User.objects.all().delete()
        Role.objects.create(name='admin')
        admin =User.objects.create_user(username='admin', password='testpass', is_superuser=True, is_staff=True)
        admin.roles.add(Role.objects.get(name='admin'))
        usr1= User.objects.create_user(username='testuser1', password='testpass')
        usr2 = User.objects.create_user(username='testuser2', password='testpass')
        for user in User.objects.all():
            print(f"User: {user.username}, ID: {user.id}, Roles: {[role.name for role in user.roles.all()]} ")
        self.stdout.write(self.style.SUCCESS(f"Deleted records"))

