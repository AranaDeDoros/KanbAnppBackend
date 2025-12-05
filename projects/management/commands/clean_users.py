from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Role

class Command(BaseCommand):
    help = "Cleans users and resets to default admin and test users"

    def handle(self, *args, **kwargs):
        User.objects.all().delete()
        Role.objects.get_or_create(name=Role.ADMIN)
        Role.objects.get_or_create(name=Role.COLLABORATOR)
        admin =User.objects.create_user(username='admin', password='testpass', is_superuser=True, is_staff=True)
        admin.roles.add(Role.objects.get(name=Role.ADMIN))
        usr1= User.objects.create_user(username='testuser1', password='testpass')
        usr1.roles.add(Role.objects.get(name=Role.COLLABORATOR))
        usr2 = User.objects.create_user(username='testuser2', password='testpass')
        usr2.roles.add(Role.objects.get(name=Role.COLLABORATOR))
        for user in User.objects.all():
            print(f"User: {user.username}, ID: {user.id}, Roles: {[role.name for role in user.roles.all()]} ")
        self.stdout.write(self.style.SUCCESS(f"Deleted records"))

