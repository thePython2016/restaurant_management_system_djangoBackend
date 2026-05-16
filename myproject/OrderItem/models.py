from django.db import models
from Order.models import Order
from Items.models import Item

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item.itemName} (x{self.quantity})"
    class Meta:
        db_table = "orderitem"  # custom table name