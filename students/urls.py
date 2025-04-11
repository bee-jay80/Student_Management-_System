from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, CustomTokenObtainPairView, CustomTokenRefreshView, ProtectedStudentView, ChangePasswordView,CourseViewSet,ProfileImageViewSet
from .forgot_password_view import ForgotPasswordView, ResetPasswordView
router = DefaultRouter()
router.register(r'student', StudentViewSet, basename='student')
router.register(r'course', CourseViewSet, basename='course')
router.register(r'profile-image', ProfileImageViewSet, basename='profile-image')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedStudentView.as_view(), name='protected_view'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password')
]