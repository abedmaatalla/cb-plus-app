from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils.timezone import now
import uuid
from main.constants import SYNC_ACTIONS


class Product(models.Model):
    id = models.CharField(max_length=13, primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    expired_at = models.DateField()


class SyncRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    record_id = models.CharField(max_length=100)
    action_at = models.DateField(default=now())
    data = models.TextField(null=True, blank=True)
    synced_at = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=SYNC_ACTIONS, default="SAVE")


import main.signals