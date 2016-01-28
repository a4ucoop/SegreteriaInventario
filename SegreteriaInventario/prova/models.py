from django.db import models

class AccurateLocation(models.Model):
	location = models.CharField(max_length=2000)

	def __str__(self):		# __unicode__ on Python 2
		return self.location

class Item(models.Model):
	item_id = models.IntegerField(default=None)
	description = models.CharField(max_length=400)
	purchase_date = models.DateTimeField('purchase date')
	price = models.DecimalField(max_digits=12, decimal_places=2)
	location = models.CharField(max_length=2000)
	accurate_location = models.ForeignKey(AccurateLocation, null=True, on_delete=models.SET_NULL)
	depreciation_starting_date = models.DateTimeField('depreciation starting date')
	residual_value = models.DecimalField(max_digits=12, decimal_places=2)
	picture = models.FileField(upload_to='pictures/%Y/%m/%d', null=True)
