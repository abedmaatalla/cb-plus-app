from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class DriverConsumer(AsyncJsonWebsocketConsumer):
    driver = None
    room_name = None

    async def connect(self):
        from .models import Driver
        self.driver = Driver.objects.get(id=self.scope["url_route"]["kwargs"]["driver_id"])

        self.room_name = 'DRIVER{}'.format(self.driver.id)
        await self.accept()
        await self.channel_layer.group_add(self.room_name, self.channel_name)

    async def disconnect(self, close_code):
        if self.driver:
            await self.channel_layer.group_discard(self.room_name, self.channel_name)
        await self.close()

    async def receive_json(self, content, **kwargs):
        print("Received event: {}".format(content))
        await self.channel_layer.group_send(self.room_name, content)

    async def request_new(self, event):
        print("Received request new: {}".format(event))
        await self.send_json(
            {
                'type': 'request.new',
                'content': event
            }
        )


class RequestConsumer(AsyncJsonWebsocketConsumer):
    request = None
    room_name = ''

    async def connect(self):
        from .models import Request
        self.request = Request.objects.get(id=self.scope["url_route"]["kwargs"]["request_id"])
        self.room_name = 'REQUEST{}'.format(self.request.id)
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if self.request:
            await self.channel_layer.group_discard(self.room_name, self.channel_name)
        await self.close()

    async def receive_json(self, content, **kwargs):
        print("Received event: {}".format(content))
        await self.channel_layer.group_send(self.room_name, content)

    async def request_statusChange(self, event):
        print("Received request status change: {}".format(event))

        await self.send_json(
            event
        )

    async def request_drivers(self, event):
        print("Received request status change: {}".format(event))
        from main.algorithms import match_driver

        await self.send_json(
            {
                "drivers": match_driver(self.request).count()
            }
        )

    async def driver_location(self, event):
        print("driver location: {}".format(event))
        await self.send_json(
            {
                'type': 'driver.location',
                'content': event
            }
        )
