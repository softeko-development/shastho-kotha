from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DoctorRequestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.doctor_id = self.scope['url_route']['kwargs']['doctor_id']
        self.group_name = f'doctor_requests_group_{self.doctor_id}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def send_update(self, event):
        data = event['data']
        await self.send(text_data=json.dumps({
            'type': 'update',
            'data': data,
        }))


# class DoctorCallNotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.doctor_id = self.scope['url_route']['kwargs']['doctor_id']
#         self.group_name = f'doctor_call_notifications_{self.doctor_id}'  

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         # Handle incoming WebSocket messages (if any)
#         pass

#     # Method to send a call notification to the doctor
#     async def send_call_notification(self, event):
#         data = event['data']
#         await self.send(text_data=json.dumps({
#             'type': 'call_notification',
#             'data': data,
#         }))


class DoctorCallNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.doctor_id = self.scope['url_route']['kwargs']['doctor_id']
        self.group_name = f'doctor_call_notifications_{self.doctor_id}'  
        self.group_name_all = 'doctor_call_notifications_all'

        print(f"Connecting to group: {self.group_name} and {self.group_name_all} for doctor ID: {self.doctor_id}")
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.channel_layer.group_add(
            self.group_name_all,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

        await self.channel_layer.group_discard(
            self.group_name_all,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming messages if needed
        pass

    async def send_call_notification(self, event):
        data = event['data']
        print("Sending call notification:", data) 
        await self.send(text_data=json.dumps({
            'type': 'call_notification',
            'data': data,
        }))

    async def send_call_status_update(self, event):
        data = event['data']
        print("Sending call status update:", data)  # Log the data being sent
        await self.send(text_data=json.dumps({
            'type': 'call_status_update',
            'data': data,
        }))



# class DoctorCallNotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.doctor_id = self.scope['url_route']['kwargs']['doctor_id']
#         self.group_name = f'doctor_call_notifications_{self.doctor_id}'  
#         self.group_name_all = 'doctor_call_notifications_all'

#         print(f"Connecting to group: {self.group_name} and {self.group_name_all} for doctor ID: {self.doctor_id}")
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         await self.channel_layer.group_add(
#             self.group_name_all,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
        
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#         await self.channel_layer.group_discard(
#             self.group_name_all,
#             self.channel_name
#         )

#     async def receive(self, text_data):
        
#         pass

#     async def send_call_notification(self, event):
#         data = event['data']
#         print("Sending call notification:", data) 
#         await self.send(text_data=json.dumps({
#             'type': 'call_notification',
#             'data': data,
#         }))


class QueueUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user_type = self.scope['url_route']['kwargs']['user_type']
        self.group_name = f'queue_updates_{self.user_type}_{self.user_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_queue_position(self, event):
        queue_position = event['queue_position']
        await self.send(text_data=json.dumps({
            'type': 'queue_update',
            'queue_position': queue_position,
        }))