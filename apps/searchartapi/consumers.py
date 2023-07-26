# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add your authentication or permission checks here if needed
        await self.accept()

    async def disconnect(self, close_code):
        # Clean up any resources if needed
        pass

    async def progress_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message,
        }))
