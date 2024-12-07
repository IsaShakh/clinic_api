from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter

from app.models import Consultation, Doctor, Patient, Clinic
from .serializers import (
    ConsultationSerializer, DoctorSerializer, PatientSerializer, ClinicSerializer
)
from app.api.permissions import IsAdminOrReadOnly, IsDoctor, IsPatient


class ConsultationViewSet(viewsets.ModelViewSet):
    """
    Вывод консультаций, их создание, а также изменение и удаление;
    Врачи и пациенты могут только просматривать свои консультации.
    Поддерживается поиск по ФИО и фильтр по статусу.
    """
    queryset = Consultation.objects.select_related('doctor', 'patient').all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['doctor__user__last_name', 'patient__user__last_name']
    ordering_fields = ['created_at']

    def get_queryset(self):
        """
        Фильтрует консультации в зависимости от роли пользователя.
        """
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role == 'doctor':
            return self.queryset.filter(doctor__user=user)
        elif user.role == 'patient':
            return self.queryset.filter(patient__user=user)
        else:
            raise PermissionDenied("Нет прав для выполнения операции")

    def get_object(self):
        """
        Проверяет права доступа при доступе к объекту.
        Врачи и пациенты могут просматривать только свои консультации.
        """
        obj = super().get_object()
        user = self.request.user
        if user.role == 'doctor' and obj.doctor.user != user:
            raise PermissionDenied("Вы можете просмотреть только свои консультации")
        if user.role == 'patient' and obj.patient.user != user:
            raise PermissionDenied("Вы можете просмотреть только свои консультации")
        return obj

    def perform_create(self, serializer):
        """
        Создание консультации доступно только администраторам.
        """
        user = self.request.user
        if user.role != 'admin':
            raise PermissionDenied("Вы не можете создать консультацию")
        serializer.save()

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsDoctor])
    def change_status(self, request, pk=None):
        """
        Изменение статуса консультации, доступно только врачам
        """
        try:
            consultation = self.get_object()
        except Consultation.DoesNotExist:
            return Response({"detail": "Консультация не найдена"}, status=status.HTTP_404_NOT_FOUND)

        if consultation.doctor.user != request.user:
            raise PermissionDenied("Вы не можете менять статус чужой консультации")

        new_status = request.data.get('status')
        if new_status not in dict(Consultation.STATUS):
            return Response({"detail": "Такого статуса нет"}, status=status.HTTP_400_BAD_REQUEST)

        consultation.status = new_status
        consultation.save()
        return Response({"detail": "Статус обновлен"}, status=status.HTTP_200_OK)


class DoctorViewSet(viewsets.ModelViewSet):
    """
    Лист врачей и изменение информации о врачах
    """
    queryset = Doctor.objects.prefetch_related('clinics').all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]  
    filter_backends = [SearchFilter]
    search_fields = ['user__last_name', 'user__first_name', 'specialization']

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        """
        Создание нового врача доступно только для администраторов
        """
        user = self.request.user
        if not user.is_staff: 
            raise PermissionDenied("Вы не можете создать врача")
        serializer.save()


class PatientViewSet(viewsets.ModelViewSet):
    """
    Лист пациентов и изменение информации о пациентах.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly] 
    filter_backends = [SearchFilter]
    search_fields = ['user__last_name', 'user__first_name', 'email']

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        """
        Создание нового пациента доступно только для администраторов
        """
        user = self.request.user
        if not user.is_staff:
            raise PermissionDenied("Вы не можете создать пациента")
        serializer.save()


class ClinicViewSet(viewsets.ModelViewSet):
    """
    Лист клиник и изменение информации о клиниках
    """
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]  
    
    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        """
        Создание новой клиники доступно только для администраторов
        """
        user = self.request.user
        if not user.is_staff:
            raise PermissionDenied("Вы не можете создать клинику")
        serializer.save()