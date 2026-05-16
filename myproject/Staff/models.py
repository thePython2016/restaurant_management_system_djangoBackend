# Staff/models.py
from django.db import models

class Staff(models.Model):
    phone = models.CharField(max_length=20, primary_key=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    address = models.CharField(max_length=255)
    region = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    
    class Meta:
        db_table = "Staff"