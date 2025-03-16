from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SEOViewSet

# Создаем роутер для ViewSet
router = DefaultRouter()
router.register(r'seo', SEOViewSet, basename='seo')

urlpatterns = [
    path('', include(router.urls)),  # Подключаем маршруты для SEO
]