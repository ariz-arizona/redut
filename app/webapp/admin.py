from django.contrib import admin
from django.utils.html import format_html

from .models import Page, Block, Image, SiteSettings


# Инлайн для изображений
class ImageInline(admin.StackedInline):
    model = Image
    extra = 1


# Админка для блоков
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
    )
    list_filter = ("type", "page")
    search_fields = ("type", "title", "menu_title", "content")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ImageInline]


# Инлайн для блоков на страницах
class BlockInline(admin.StackedInline):
    model = Block
    extra = 1
    fields = (
        "type",
        "order",
        "title",
        "sub_title",
        "menu_title",
        "slug",
        "content",
        "page",
    )
    fk_name = "page"
    ordering = ["order"]
    inlines = [ImageInline]


# Админка для страниц
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_homepage")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [BlockInline]  # Добавляем инлайн для блоков


# Админка для изображений
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("title", "image", "alt_text", "block", "order")
    list_filter = ("block",)
    search_fields = ("alt_text", "title")


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
