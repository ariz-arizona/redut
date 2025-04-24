from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PageViewSet,
    EnabledSiteSettingsView,
    FeedbackViewSet,
    CategoryViewSet,
)

# Создаем роутер для ViewSet
router = DefaultRouter()
router.register(r"page", PageViewSet)
router.register(r"feedback", FeedbackViewSet)
router.register(r"cat", CategoryViewSet)

urlpatterns = [
    path("site-settings/", EnabledSiteSettingsView.as_view(), name="site-settings"),
    path("", include(router.urls)),
]
