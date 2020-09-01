from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core import serializers
from django.utils.timezone import now


class StockUser(AsyncJsonWebsocketConsumer):
    user = None
    room_name = None

    async def connect(self):
        from django.contrib.auth.models import User
        self.user = User.objects.get(id=self.scope["url_route"]["kwargs"]["user_id"])

        self.room_name = 'STOCK{}'.format(self.user.id)
        await self.accept()
        await self.channel_layer.group_add(self.room_name, self.channel_name)

    async def disconnect(self, close_code):
        if self.user:
            await self.channel_layer.group_discard(self.room_name, self.channel_name)
        await self.close()

    async def receive_json(self, content, **kwargs):
        print("Received event: {}".format(content))
        await self.channel_layer.group_send(self.room_name, content)

    async def stock(self, event):
        print("Received request new: {}".format(event))
        await self.send_json(event)

    async def sync_from(self, event):
        print("Received request new: {}".format(event))
        """
            send list of un-synced data
        """
        from main.models import SyncRecord
        qs = SyncRecord.objects.filter(user=self.user, synced_at=None)
        qs_json = serializers.serialize('json', qs)
        await self.send_json(qs_json)

    async def sync_to(self, event):
        print("Received request new: {}".format(event))
        """
        data
            stock_dict
            action_at 
            action 
        """
        if "stock_dict" in event and "action_at" in event and "action" in event:
            if "id" in event['stock_dict']:
                from main.models import SyncRecord
                sync_records = SyncRecord.objects.filter(record_id=event['stock_dict']['id'], action_at__gte=event['action_at'])
                if not sync_records:
                    SyncRecord.objects.filter(record_id=event['stock_dict']['id'], action_at__lte=event['action_at']).update(
                        synced_at=now())
                    from main.models import Stock
                    stock = Stock.objects.filter(id=event['stock_dict']['id']).first()
                    if stock:
                        if event['action'] == "CREATE":
                            print("create")
                            await self.send_json(
                                {"message": "Successfully synced", "error": False})
                            return
                        if event['action'] == "UPDATE":
                            print('update')

                            await self.send_json(
                                {"message": "Successfully synced", "error": False})
                            return
                        if event['action'] == "DELETE":
                            print("delete")
                            await self.send_json(
                                {"message": "Successfully synced", "error": False})
                            return

        await self.send_json({"message": "there is newer data in server. Please sync from server", "error": True})

    async def synced(self, event):
        print("Received request new: {}".format(event))
        """
        data
            - sync_record_id 
        """

        if "sync_record_id" in event:
            print(event['sync_record_id'])
            from main.models import SyncRecord
            synced_record = SyncRecord.objects.filter(id=event['sync_record_id'])
            if synced_record:
                synced_record.update(synced_at=now())
                await self.send_json({'message': "Success", "error": False})
                return

        await self.send_json({'message': "Failed", "error": True})
