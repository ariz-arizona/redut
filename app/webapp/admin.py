from django.contrib import admin
from django.utils.html import format_html

from .models import Page, Block, Image, SiteSettings, Feedback


# Инлайн для изображений
class ImageInline(admin.StackedInline):
    model = Image
    extra = 1


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "page",
        "type",
        "order",
        "sub_title",
        "menu_title",
        "slug",
        "is_text_right",  # Новое поле
    )
    list_filter = ("type", "page", "is_text_right")  # Фильтр по новому полю
    search_fields = ("type", "title", "menu_title", "content")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ImageInline]

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "type",
                    "title",
                    "sub_title",
                    "slug",
                    "order",
                    "is_text_right",  # Поле для текста справа/слева
                ),
            },
        ),
        (
            "Ссылки",
            {
                "fields": (
                    "link",
                    "external_link",
                ),
            },
        ),
        (
            "Контент",
            {
                "fields": (
                    "content",
                    "content_rendered",  # Отрендеренный контент (только для чтения)
                ),
            },
        ),
        (
            "Меню",
            {
                "fields": ("menu_title",),
            },
        ),
        (
            "Привязка к странице",
            {
                "fields": ("page",),
            },
        ),
    )

    readonly_fields = (
        "content_rendered",
    )  # Делаем отрендеренный контент только для чтения
    
class BlockInline(admin.StackedInline):
    model = Block
    extra = 1
    fk_name = "page"
    ordering = ["order"]
    inlines = [ImageInline]

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "type",
                    "title",
                    "sub_title",
                    "slug",
                    "order",
                    "is_text_right",
                ),
            },
        ),
        (
            "Ссылки",
            {
                "fields": (
                    "link",
                    "external_link",
                ),
            },
        ),
        (
            "Контент",
            {
                "fields": (
                    "content",
                ),
            },
        ),
    )


# Админка для страниц
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_homepage")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [BlockInline]  # Добавляем инлайн для блоков

class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "block",
        "order",
        "alt_text",
        "url",
    )
    list_filter = ("block",)  # Фильтр по блокам
    search_fields = ("title", "alt_text")  # Поиск по заголовку и альтернативному тексту
    ordering = ["order"]  # Сортировка по порядку

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "block",
                    "image",
                    "alt_text",
                    "title",
                    "order",
                ),
            },
        ),
        (
            "Ссылки",
            {
                "fields": (
                    "url",
                ),
            },
        ),
        (
            "Контент",
            {
                "fields": (
                    "text",
                    "text_rendered",  # Отрендеренный контент (только для чтения)
                ),
            },
        ),
    )

    readonly_fields = ("text_rendered",)  # Делаем отрендеренный контент только для чтения

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Админка для модели SiteSettings.
    """

    list_display = ("phone_number", "logo_preview", "footer_text_short", "is_enabled")
    list_filter = ("is_enabled",)
    search_fields = ("phone_number", "footer_text")
    actions = ["make_enabled"]

    fieldsets = (
        (
            None,
            {
                "fields": ("phone_number", "logo", "footer_text", "is_enabled"),
            },
        ),
    )

    def logo_preview(self, obj):
        """
        Возвращает HTML-представление логотипа для предпросмотра.
        """
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" />', obj.logo.url)
        return "Нет логотипа"

    logo_preview.short_description = "Логотип"

    def footer_text_short(self, obj):
        """
        Возвращает укороченную версию текста футера.
        """
        return (
            obj.footer_text[:50] + "..."
            if len(obj.footer_text) > 50
            else obj.footer_text
        )

    footer_text_short.short_description = "Текст футера"

from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "created_at",
        "has_message",  # Показывает, есть ли сообщение
    )
    list_filter = ("created_at",)  # Фильтр по дате создания
    search_fields = ("name", "phone")  # Поиск по имени и телефону
    readonly_fields = ("created_at",)  # Дата создания только для чтения

    @admin.display(description="Есть сообщение?", boolean=True)
    def has_message(self, obj):
        """
        Проверяет, есть ли текст в поле `message`.
        """
        return bool(obj.message)