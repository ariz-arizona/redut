from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SEO
from .serializers import SEOSerializer

class SEOViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с SEO данными.
    """
    queryset = SEO.objects.all().order_by('-created_at')  # Сортировка по дате создания
    serializer_class = SEOSerializer
