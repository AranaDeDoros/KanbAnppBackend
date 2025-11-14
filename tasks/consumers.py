import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Unir al grupo común de tareas (podrías tenerlo por proyecto)
        self.room_group_name = "tasks_updates"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Aquí podrías manejar mensajes entrantes (no requerido si solo es broadcast)
        print("Received:", data)

    async def task_update(self, event):
        """Recibe actualizaciones desde el backend y las manda al frontend"""
        await self.send(text_data=json.dumps(event["data"]))
