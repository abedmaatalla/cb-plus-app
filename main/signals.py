from time import sleep

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.utils.timezone import now
from django.contrib.auth.models import User

from models import Stock, SyncRecord


@receiver(post_save, sender=Stock, dispatch_uid="app_notification")
def driver_notification(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    print("user")

    candidates = User.objects.all()
    request_type = "stock.save"
    if created:
        request_type = "stock.create"
    for candidate in candidates:
        async_to_sync(channel_layer.group_send)(
            "STOCK{}".format(candidate.id),
            {"type": request_type, "content": {"stock_id": str(instance.id)}}
        )


@receiver(post_delete, sender=Stock, dispatch_uid="app_notification")
def driver_notification(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()

    candidates = User.objects.all()

    for candidate in candidates:
        async_to_sync(channel_layer.group_send)(
            "STOCK{}".format(candidate.id),
            {"type": "stock.delete", "content": {"stock_id": str(instance.id)}}
        )
