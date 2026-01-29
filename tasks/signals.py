from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Task
from .serializers import TaskSerializer
"""used in websocket to notify clients about task updates"""
#@receiver(post_save, sender=Task)
def notify_task_update(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    data = TaskSerializer(instance).data

    async_to_sync(channel_layer.group_send)(
        "tasks_updates",
        {
            "type": "task_update",
            "data": data,
        },
    )

