from django.db import models

# Create your models here.
class Item(models.Model):
    def __str__(self):
        return self.item_name

    item_name=models.CharField(max_length=300)
    item_desc=models.CharField(max_length=400)
    item_price=models.FloatField()
