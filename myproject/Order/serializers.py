

from rest_framework import serializers
from .models import Order
from OrderItem.serializers import OrderItemSerializer

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'