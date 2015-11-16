from django.db import models

class Item(models.Model):
	item_id = models.IntegerField(default=None)
	description = models.CharField(max_length=400)
	purchase_date = models.DateTimeField('purchase date')
	price = models.DecimalField(max_digits=12, decimal_places=2)
	location = models.CharField(max_length=2000)
	depreciation_starting_date = models.DateTimeField('depreciation starting date')