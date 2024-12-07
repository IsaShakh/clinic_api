from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Clinic(models.Model):
    name = models.CharField(max_length=150)
    ur_adress = models.CharField(max_length=150)
    fact_adress = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    role = models.CharField(choices=ROLES, max_length=10)
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups", 
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  
        blank=True
    )
    
    
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12)
    email = models.EmailField()
        
        
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=150)
    clinics = models.ManyToManyField(Clinic, related_name='clinics')
    
    
class Consultation(models.Model):
    STATUS = [
        ('confirmed', 'Подтверждена'),
        ('pending', 'Ожидает'),
        ('started', 'Начата'),
        ('finished', 'Завершена'),
        ('paid', 'Оплачена'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient')
    
    

    