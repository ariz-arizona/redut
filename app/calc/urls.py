from django.urls import path, include
from rest_framework.routers import DefaultRouter
from calc.views import ConfigView, CalculatorDataViewSet

router = DefaultRouter()
router.register(r"data", CalculatorDataViewSet)

urlpatterns = [
    path("config/", ConfigView.as_view(), name="config"),
    path("", include(router.urls)),
]
