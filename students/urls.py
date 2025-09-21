from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentRegisterViewSet, StudentViewSet, LoginViewSet, LogoutViewSet, ProtectedStudentViewSet, ChangePasswordViewSet,CourseViewSet,ProfileImageViewSet
from .forgot_password_view import ForgotPasswordViewSet, ResetPasswordViewSet
router = DefaultRouter()

router.register(r'register', StudentRegisterViewSet, basename='register')
router.register(r'student', StudentViewSet, basename='student')
router.register(r'course', CourseViewSet, basename='course')
router.register(r'profile-image', ProfileImageViewSet, basename='profile-image')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'logout', LogoutViewSet, basename='logout')
router.register(r'protected', ProtectedStudentViewSet, basename='protected')
router.register(r'change-password', ChangePasswordViewSet, basename='change-password')
router.register(r'forgot-password', ForgotPasswordViewSet, basename='forgot-password')
router.register(r'reset-password', ResetPasswordViewSet, basename='reset-password')

urlpatterns = [
    path('', include(router.urls)),
]