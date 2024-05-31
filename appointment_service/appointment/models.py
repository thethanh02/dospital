from djongo import models
from case.models import Case

class Appointment(models.Model):
	patient = models.IntegerField() # User
	receptionist = models.IntegerField() # User
	doctor = models.IntegerField() # User
	case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='appointment_case')
	appointment_time = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.patient + ' with ' + self.doctor