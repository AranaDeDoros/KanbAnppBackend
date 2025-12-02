from django.core.management.base import BaseCommand
from projects.models import Project
from tasks.models import Task

class Command(BaseCommand):
    help = "Cleans old model records"

    def handle(self, *args, **kwargs):
        #empty tasks
        deletedTask = Task.objects.filter().delete()
        #delete all but one first project
        deletedProjects = Project.objects.filter(id__gt=1).delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted records"))

