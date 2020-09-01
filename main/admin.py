from django.contrib import admin

# Register your models here.
from main.models import Product, Stock, SyncRecord


@admin.register(Product)
class CostumerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Stock)
class CostumerAdmin(admin.ModelAdmin):
    list_display = ('product', 'expired_at')
    search_fields = ('product', 'expired_at')


@admin.register(SyncRecord)
class CostumerAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'action_at', 'action')
    search_fields = ('record_id', 'action_at', 'action')
