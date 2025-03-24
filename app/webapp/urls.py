from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PageViewSet, EnabledSiteSettingsView

# Создаем роутер для ViewSet
router = DefaultRouter()
router.register(r"page", PageViewSet)

urlpatterns = [
    path("site-settings/", EnabledSiteSettingsView.as_view(), name="site-settings"),
    path("", include(router.urls)),
]
