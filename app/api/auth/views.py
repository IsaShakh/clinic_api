from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .serializers import DoctorRegistrationSerializer, PatientRegistrationSerializer, UserSerializer, UserUpdateSerializer

class UserRegistrationView(generics.CreateAPIView):
    """
    Регистрация юзера
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'id': user.id,
            'username': user.username,
            'role': user.role
        }, status=status.HTTP_201_CREATED)


class PatientRegistrationView(generics.CreateAPIView):
    """
    Регистрация пациента
    """
    serializer_class = PatientRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()
        return Response({
            'id': patient.id,
            'username': patient.user.username,
            'role': patient.user.role,
            'phone': patient.phone,
            'email': patient.email
        }, status=status.HTTP_201_CREATED)
        
        
class DoctorRegistrationView(generics.CreateAPIView):
    """
    Регистрация доктора
    """
    serializer_class = DoctorRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor = serializer.save()
        return Response({
            'id': doctor.id,
            'username': doctor.user.username,
            'role': doctor.user.role,
            'specialization': doctor.specialization,
            'clinics': [clinic.id for clinic in doctor.clinics.all()]
        }, status=status.HTTP_201_CREATED)
        
        
class UserUpdateView(generics.UpdateAPIView):
    """
    Обновление пользователя
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'id': user.id,
            'username': user.username,
            'role': user.role
        }, status=status.HTTP_200_OK)