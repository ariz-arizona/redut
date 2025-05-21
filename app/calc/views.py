from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Range, AdditionalService, CalculatorData
from .serializers import (
    RangeSerializer,
    AdditionalServiceSerializer,
    CalculatorDataSerializer,
)


class ConfigView(APIView):
    def get(self, request):
        ranges = Range.objects.all()
        services = AdditionalService.objects.filter(is_active=True)

        config = {
            "ranges": RangeSerializer(ranges, many=True).data,
            "services": AdditionalServiceSerializer(services, many=True).data,
        }

        return Response(config)


class CalculatorDataViewSet(viewsets.ModelViewSet):
    queryset = CalculatorData.objects.all().order_by("-created_at")
    serializer_class = CalculatorDataSerializer
