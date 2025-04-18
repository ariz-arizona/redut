from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .models import Page, SiteSettings, Feedback

from .serializers import SiteSettingsSerializer, PageSerializer, FeedbackSerializer


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    lookup_field = "slug"  # Используем slug вместо id для поиска

    def list(self, request, *args, **kwargs):
        """
        Переопределяем метод list, чтобы возвращать только главную страницу.
        """
        homepage = Page.objects.filter(is_homepage=True).first()
        if not homepage:
            return Response(
                {"detail": "Главная страница не найдена."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(homepage)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Переопределяем метод retrieve, чтобы искать страницу по slug.
        """
        slug = kwargs.get("slug")
        page = get_object_or_404(Page, slug=slug)
        serializer = self.get_serializer(page)
        return Response(serializer.data)


class EnabledSiteSettingsView(APIView):
    """
    Возвращает активные настройки сайта (is_enabled=True).
    """

    def get(self, request, *args, **kwargs):
        # Получаем активную запись
        site_settings = SiteSettings.get_enabled()

        if site_settings:
            # Сериализуем данные
            serializer = SiteSettingsSerializer(site_settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Если активной записи нет
            return Response(
                {"detail": "Активные настройки сайта не найдены."},
                status=status.HTTP_404_NOT_FOUND,
            )


class FeedbackThrottle(AnonRateThrottle):
    """
    Ограничение на количество запросов с одного IP-адреса.
    """

    rate = "1/minute"


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]  # Разрешаем доступ без аутентификации
    throttle_classes = [FeedbackThrottle]  # Добавляем ограничение
