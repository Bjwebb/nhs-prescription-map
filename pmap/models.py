from django.db import models

class ItemLocation(models.Model):
    item_id = models.CharField(max_length=50)
    item_name = models.CharField(max_length=256)
    lat = models.FloatField()
    lon = models.FloatField()
    quantity = models.IntegerField()
