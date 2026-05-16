from django.db import models

# Create your models here.


class InventoryItems(models.Model):
    date = models.DateField()
    itemID = models.ForeignKey('Items.Item', on_delete=models.CASCADE, db_column='itemID', related_name='inventory_items', null=True, blank=True)
    item_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.item_name} ({self.quantity})"

    class Meta:
        db_table = "InventoryItems"  # custom table name