from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def broadcast_task(task_data):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "tasks_updates",
        {
            "type": "task_update",
            "data": task_data,
        },
    )