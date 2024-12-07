from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter
from app.api.crud.views import ConsultationViewSet, DoctorViewSet, PatientViewSet, ClinicViewSet
from app.api.auth.views import DoctorRegistrationView, PatientRegistrationView, UserRegistrationView, UserUpdateView
  
router = DefaultRouter()

router.register(r'consultations', ConsultationViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'clinics', ClinicViewSet)

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/user/', UserRegistrationView.as_view(), name='user-registration'),
    path('register/patient/', PatientRegistrationView.as_view(), name='patient-register'),
    path('register/doctor/', DoctorRegistrationView.as_view(), name='doctor-registration'),
    path('update/user/', UserUpdateView.as_view(), name='user-update'),
] + router.urls
