from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.throttling import AnonRateThrottle

from django_filters.rest_framework import DjangoFilterBackend

from .models import Page, SiteSettings, Feedback, Category

from .serializers import (
    SiteSettingsSerializer,
    PageSerializer,
    FeedbackSerializer,
    CategorySerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().prefetch_related("pages")
    serializer_class = CategorySerializer
    lookup_field = "slug"  # Используем slug вместо id для поиска


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    lookup_field = "slug"  # Используем slug вместо id для поиска
    filter_backends = [DjangoFilterBackend]  # Добавляем поддержку фильтрации
    filterset_fields = {
        'category__slug': ['exact'],  # Фильтрация по category__slug
    }

    def retrieve(self, request, *args, **kwargs):
        """
        Если slug == 'homepage' — возвращаем главную страницу.
        Иначе — стандартное поведение (поиск по slug).
        """
        slug = self.kwargs.get("slug")

        if slug == "homepage":
            page = Page.objects.filter(is_homepage=True).first()
            if not page:
                raise NotFound({"detail": "Главная страница не найдена."})
        else:
            page = self.get_queryset().filter(slug=slug).first()
            if not page:
                raise NotFound({"detail": f"Страница с slug='{slug}' не найдена."})

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
