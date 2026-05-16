from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['itemID', 'itemName', 'description', 'category', 'unitOfMeasure', 'dateAdded']
        extra_kwargs = {
            # Allow creating without description or with an empty string
            'description': {'required': False, 'allow_blank': True},
            'unitOfMeasure': {'required': True, 'allow_blank': False},
            # dateAdded is optional because model has a default
            'dateAdded': {'required': True},
        }