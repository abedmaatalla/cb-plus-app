from dynamic_rest.fields import DynamicRelationField
from rest_framework import serializers

from main.models import Stock, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    duration = serializers.DurationField(read_only=True)
    class Meta:
        model = Stock
        fields = ('id', 'product', 'expired_at', 'duration')
