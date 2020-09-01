from django.contrib import admin

# Register your models here.
from models import Product, Stock


@admin.register(Product)
class CostumerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Stock)
class CostumerAdmin(admin.ModelAdmin):
    list_display = ('product', 'expired_at')
    search_fields = ('product', 'expired_at')
