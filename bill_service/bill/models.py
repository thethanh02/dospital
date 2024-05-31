from django.db import models

class Bill(models.Model):
	case = models.IntegerField()
	ammount = models.IntegerField()
	item = models.IntegerField()
	quantity = models.IntegerField()
	bill_date = models.DateField()
	bill_details = models.CharField(max_length=200)
	is_paid = models.BooleanField(default=False)
