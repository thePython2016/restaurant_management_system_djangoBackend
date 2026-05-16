from django.db import models

# Create your models here.
class Payment(models.Model):
    paymentID = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order.Order', on_delete=models.CASCADE, related_name="payments")
    customer = models.ForeignKey('Customer.Customer', on_delete=models.CASCADE, related_name="payments")
    paymentName = models.CharField(max_length=100)
    paymentDate = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment {self.paymentID} - {self.amount}"

    class Meta:
        app_label = 'Payment'
        db_table = "Payment"  # custom table name