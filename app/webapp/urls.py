from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PageViewSet

# Создаем роутер для ViewSet
router = DefaultRouter()
router.register(r'page', PageViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Подключаем маршруты для SEO
]