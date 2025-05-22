from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Range, AdditionalService, CalculatorData, BaseRate
from .serializers import (
    RangeSerializer,
    AdditionalServiceSerializer,
    CalculatorDataSerializer,
)


class ConfigView(APIView):
    def get(self, request):
        ranges = Range.objects.all()
        services = AdditionalService.objects.filter(is_active=True)
                # Получаем активную ставку
        base_rate = BaseRate.objects.filter().first()  # Предположим, что только одна запись или ты сам управляешь
        base_rate_value = float(base_rate.rate) if base_rate else 15.0  # fallback, если ставка не задана


        config = {
            "ranges": RangeSerializer(ranges, many=True).data,
            "services": AdditionalServiceSerializer(services, many=True).data,
                        "base_rate": base_rate_value

        }

        return Response(config)


class CalculatorDataViewSet(viewsets.ModelViewSet):
    queryset = CalculatorData.objects.all().order_by("-created_at")
    serializer_class = CalculatorDataSerializer
