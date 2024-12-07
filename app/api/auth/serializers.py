from django.contrib.auth import get_user_model
from rest_framework import serializers
from app.models import Clinic, Doctor, Patient
from app.api.crud.serializers import ClinicSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password) 
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
    
    
class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
    
    
class PatientRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Используем PrimaryKey для связи с пользователем

    class Meta:
        model = Patient
        fields = ['user', 'phone', 'email']

    def create(self, validated_data):
        # Получаем пользователя по ID из данных
        user = validated_data.pop('user')
        
        # Создаем пациента, привязывая его к существующему пользователю
        patient = Patient.objects.create(user=user, **validated_data)
        return patient

    def update(self, instance, validated_data):
        # Получаем пользователя по ID
        user = validated_data.pop('user')

        # Обновляем информацию о пользователе
        instance.user = user
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance

    
    
class DoctorRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Используем PrimaryKey для связи с пользователем
    clinics = serializers.PrimaryKeyRelatedField(queryset=Clinic.objects.all(), many=True)  # Используем PrimaryKey для клиник

    class Meta:
        model = Doctor
        fields = ['user', 'specialization', 'clinics']

    def create(self, validated_data):
        # Получаем пользователя и клиники по ID из данных
        user = validated_data.pop('user')
        clinics = validated_data.pop('clinics')
        
        # Создаем доктора
        doctor = Doctor.objects.create(user=user, **validated_data)

        # Привязываем клиники к доктору
        doctor.clinics.set(clinics)
        return doctor

    def update(self, instance, validated_data):
        # Получаем пользователя и клиники по ID
        user = validated_data.pop('user')
        clinics = validated_data.pop('clinics')

        # Обновляем информацию о пользователе
        instance.user = user
        instance.specialization = validated_data.get('specialization', instance.specialization)

        # Обновляем клиники
        instance.clinics.set(clinics)
        instance.save()

        return instance