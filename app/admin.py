from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Patient, Doctor, Clinic, Consultation


class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    verbose_name_plural = "Пациент"


class DoctorInline(admin.StackedInline):
    model = Doctor
    can_delete = False
    verbose_name_plural = "Доктор"


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'groups')
    search_fields = ('username', 'email', 'role')
    inlines = [PatientInline, DoctorInline]


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'ur_adress', 'fact_adress')
    search_fields = ('name', 'ur_adress', 'fact_adress')
    list_per_page = 25


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone')
    search_fields = ('user__username', 'email', 'phone')
    list_per_page = 25


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization')
    search_fields = ('user__username', 'specialization')
    filter_horizontal = ('clinics',)
    list_per_page = 25


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'status', 'doctor', 'patient', 'start_time', 'end_time')
    list_filter = ('status', 'doctor__user__username', 'patient__user__username', 'start_time', 'end_time')
    search_fields = ('doctor__user__username', 'patient__user__username', 'status')
    date_hierarchy = 'start_time'
    list_per_page = 25
