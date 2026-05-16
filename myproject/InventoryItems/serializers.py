from rest_framework import serializers
from .models import InventoryItems
from Items.serializers import ItemSerializer
from Items.models import Item
from datetime import date


class InventoryItemsSerializer(serializers.ModelSerializer):
    # Accept itemID as a writable primary key on input
    itemID = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    category = serializers.CharField(source='itemID.category', read_only=True)
    unit_of_measure = serializers.CharField(source='itemID.unitOfMeasure', read_only=True)

    item_pk = serializers.SerializerMethodField()

    class Meta:
        model = InventoryItems
        fields = ['id', 'date', 'itemID', 'item_name', 'description', 'quantity', 'category', 'unit_of_measure', 'item_pk']
    
    def get_item_pk(self, obj):
        return obj.itemID.itemID if obj.itemID else None  # Using itemID instead of id as it's the primary key

    def to_representation(self, instance):
        """Return nested Item data for `itemID` in responses while keeping a writable PK field."""
        ret = super().to_representation(instance)
        try:
            if instance.itemID:
                item_data = ItemSerializer(instance.itemID).data
                ret['itemID'] = {
                    'itemID': instance.itemID.itemID,  # Using correct primary key field
                    'itemName': instance.itemID.itemName,
                    'category': instance.itemID.category,
                    'unitOfMeasure': instance.itemID.unitOfMeasure
                }
                ret['category'] = instance.itemID.category
                ret['unit_of_measure'] = instance.itemID.unitOfMeasure
            else:
                ret['itemID'] = None
                ret['category'] = ''
                ret['unit_of_measure'] = ''
        except Exception as e:
            import traceback
            print(f"Error in serializer to_representation: {str(e)}")
            print(f"Full traceback: {traceback.format_exc()}")
            ret['itemID'] = None
            ret['category'] = ''
            ret['unit_of_measure'] = ''
        return ret

    def validate_date(self, value):
        """
        Validate that the date is not in the future
        """
        if value > date.today():
            raise serializers.ValidationError("Date cannot be in the future.")
        return value

    def validate_item_name(self, value):
        """
        Validate item name is not empty and has reasonable length
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Item name cannot be empty.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Item name must be at least 2 characters long.")
        return value.strip()


    # No duplicate check here; handled in viewset
