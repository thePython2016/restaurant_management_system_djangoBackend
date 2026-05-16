from django.db import models
from Customer.models import Customer
from Staff.models import Staff
from Items.models import Item

class Order(models.Model):
    orderNumber = models.AutoField(primary_key=True)
    # Store FK as column name 'customerID' to match naming preference
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="order",
        db_column="customerID",
    )
    employee = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, related_name="orders")
    itemID = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="order",
        db_column="itemID",
    )
    orderDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.orderNumber}"
    class Meta:
        db_table = "order_"  # custom table name