"""from time import sleep"""

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from main.models import Stock, SyncRecord


@receiver(post_save, sender=Stock, dispatch_uid="stock_save_notification")
def stock_save_notification(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()

    candidates = User.objects.all()
    request_type = "stock.update"
    if created:
        request_type = "stock.create"

    for candidate in candidates:
        async_to_sync(channel_layer.group_send)(
            "STOCK{}".format(candidate.id),
            {"type": "stock", "content": {"stock_id": str(instance.id), "action": request_type}}
        )
        SyncRecord.objects.create(
            content_type=ContentType.objects.get(model='stock'),
            record_id=instance.id,
            user=candidate,
            data=instance.__dict__,
            action="SAVE" if request_type == "stock.create" else "UPDATE"
        )


@receiver(pre_delete, sender=Stock, dispatch_uid="stock_delete_notification")
def stock_delete_notification(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()

    candidates = User.objects.all()
    request_type = "stock.delete"

    for candidate in candidates:
        async_to_sync(channel_layer.group_send)(
            "STOCK{}".format(candidate.id),
            {"type": "stock", "content": {"stock_id": str(instance.id), "action": request_type}}
        )
        
        SyncRecord.objects.create(
            content_type=instance.model_class(),
            record_id=instance.id,
            user=candidate,
            data=instance.__dict__,
            action="DELETE"
        )

