from django.db import models
from django.conf import settings
from projects.models import Project
from common.choices import STATUS_CHOICES
from common.choices import PRIORITIES

class Task(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='backlog')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks_assigned'
    )
    priority = models.CharField(max_length=20, choices=PRIORITIES, default='regular') #arrows, icons
    estimate_points = models.IntegerField(default=1) #regular input
    acceptance_criteria = models.TextField(default='', help_text='Acceptance Criteria') #available on click

    def __str__(self):
        return self.title


import os
import uuid
from datetime import datetime

def task_attachment_upload_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    new_filename = f"{uuid.uuid4()}.{ext}"

    today = datetime.now()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")

    return os.path.join(
        "tasks",
        str(instance.task.id),
        year,
        month,
        day,
        new_filename
    )


class TaskAttachments(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=task_attachment_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.task.title} uploaded at {self.uploaded_at}"

    def delete(self, *args, **kwargs):
        storage = self.file.storage
        path = self.file.path

        super().delete(*args, **kwargs)

        if storage.exists(path):
            storage.delete(path)

class Tag(models.Model):
    name = models.CharField(max_length=50)
    tasks = models.ManyToManyField(Task, related_name='tags')

    def __str__(self):
        return self.name