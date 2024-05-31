from djongo import models

class Case(models.Model):
	patient = models.IntegerField()
	receptionist = models.IntegerField()
	description = models.CharField(max_length=500, default=None)
	filed_date = models.DateField()
	closed_date = models.DateField(default=None, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.patient + ' having ' + self.description