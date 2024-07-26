from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'superadmin'),
        (2, 'Doctor'),
        (3, 'Patient'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=3)
    class Meta:
        app_label = 'healthapp'

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 2})
    name = models.CharField(max_length=50)
    mobile = models.IntegerField()
    special = models.CharField(max_length=50)
    about = models.CharField(max_length=50)
    image = models.ImageField(upload_to='doctors/', blank=True, null=True)

    def __str__(self):
        return self.name

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 3})
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    mobile = models.IntegerField()
    address = models.CharField(max_length=100)
    image= models.ImageField(upload_to='patients/', blank=True, null=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('REJECTED', 'Rejected'),
        ('ACCEPTED', 'Accepted'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient_name = models.CharField(max_length=50)
    symptoms = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.patient.name} - {self.date} {self.time}"




class Prescription(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    symptoms = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions_with_symptoms', null=True)
    prescription = models.CharField(max_length=2500, null=True)
    patient_name = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions_with_patient', null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')

    def __str__(self):
        return self.patient_name.patient_name

class Payment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.order_id
    
class Receipt(models.Model):
    invoice_number = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=255)
    hospital_phone = models.CharField(max_length=20)
    hospital_email = models.EmailField()
    patient_name = models.CharField(max_length=20)
    symptoms = models.CharField(max_length=20)
    doctor = models.CharField(max_length=20)
    doctor_fee = models.DecimalField(max_digits=10, decimal_places=2)
    prescription = models.CharField(max_length=20)
    prescription_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    
        