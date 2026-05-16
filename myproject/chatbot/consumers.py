import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import ChatRoom, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.create_room(self.room_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = data.get('user', 'Anonymous')

        # Save and send user message
        await self.save_message(self.room_name, user, message, False)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
                'is_bot': False
            }
        )

        # Generate and send bot response
        bot_response = self.generate_bot_response(message)
        await self.save_message(self.room_name, 'ChatBot', bot_response, True)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': bot_response,
                'user': 'ChatBot',
                'is_bot': True
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user'],
            'is_bot': event['is_bot'],
            'timestamp': timezone.now().isoformat()
        }))

    @database_sync_to_async
    def create_room(self, room_name):
        room, created = ChatRoom.objects.get_or_create(name=room_name)
        return room

    @database_sync_to_async
    def save_message(self, room_name, user, message, is_bot):
        room = ChatRoom.objects.get(name=room_name)
        return Message.objects.create(
            room=room, user=user, content=message, is_bot=is_bot
        )

    def generate_bot_response(self, user_message):
        msg = user_message.lower()
        if 'hello' in msg or 'hi' in msg:
            return "Hello! How can I help you today?"
        elif 'how are you' in msg:
            return "I'm doing great! Thanks for asking."
        elif 'bye' in msg:
            return "Goodbye! Have a great day!"
        else:
            return f"Thanks for your message: '{user_message}'. How else can I help?"