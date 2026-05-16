
from django.db import models
from Items.models import Item

class Menu(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
  
    description = models.TextField(blank=True)
    # items = models.ManyToManyField(Item, related_name='menus')
    # is_active = models.BooleanField(default=True)
    itemid = models.ForeignKey(Item, on_delete=models.CASCADE, db_column='itemid', related_name='menus')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "menuItem"  # custom table name


