from django.db import models
from Staff.models import Staff

class Customer(models.Model):
    customerID = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100,null=False,blank=False)
    phoneNumber = models.CharField(max_length=10, unique=True, null=False, blank=False)
    physicalAddress = models.CharField(max_length=255,null=False,blank=False)
    region = models.CharField(max_length=255,null=False,blank=False)
    # employee = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, related_name="customers")

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = "Customer"  # custom table name