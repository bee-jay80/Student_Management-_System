from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import GradesViewSet


router = DefaultRouter()
router.register(r'grades', GradesViewSet, basename='grades')
urlpatterns = router.urls
