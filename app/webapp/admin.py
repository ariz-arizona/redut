from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db.models import OuterRef, Subquery

from .models import (
    SiteSettings,
    Document,
    Category,
    Page,
    Block,
    Image,
    Feedback,
)


# Inline для документов в админке SiteSettings
class DocumentInline(admin.TabularInline):
    model = Document.site_settings.through
    extra = 1
    verbose_name = _("Документ")
    verbose_name_plural = _("Документы")


# Inline для изображений в блоках
class ImageInline(admin.StackedInline):
    model = Image
    extra = 1
    classes = ["collapse"]

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
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
                    "external_link",
                    "link",
                ),
                "classes": ["collapse"],
            },
        ),
        (
            "Контент",
            {
                "fields": (
                    "text",
                    "text_rendered",
                ),
                "classes": ["collapse"],
            },
        ),
    )

    readonly_fields = ("text_rendered",)


# Inline для связей "многие ко многим" между страницами и блоками
class BlockInline(admin.StackedInline):
    model = Block.pages.through
    extra = 1
    verbose_name = _("Блок")
    verbose_name_plural = _("Блоки")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone_number",
        "logo_preview",
        "footer_text_short",
        "is_enabled",
    )
    list_filter = ("is_enabled",)
    search_fields = ("phone_number", "footer_text")
    actions = ["make_enabled"]
    inlines = [DocumentInline]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "phone_number",
                    "logo",
                    "footer_text_md",
                    "footer_text",
                    "is_enabled",
                ),
            },
        ),
    )
    readonly_fields = ("footer_text",)

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


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "uploaded_at", "description_short")
    list_filter = ("uploaded_at",)
    search_fields = ("title", "description")
    readonly_fields = ("uploaded_at",)

    @admin.display(description=_("Описание"))
    def description_short(self, obj):
        """
        Отображает первые 50 символов описания.
        """
        return obj.description[:50] + "..." if obj.description else "-"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "sub_title", "slug", "pages_count")
    search_fields = ("title", "sub_title")
    prepopulated_fields = {"slug": ("title",)}  # Автозаполнение slug из title

    def pages_count(self, obj):
        """
        Возвращает количество страниц в категории.
        """
        return obj.pages.count()

    pages_count.short_description = _("Количество страниц")
    pages_count.admin_order_field = "pages__count"


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "type",
        "order",
        "sub_title",
        "menu_title",
        "slug",
        "is_text_right",
        "first_page",  # Новое поле для отображения первой страницы
    )
    list_filter = ("type", "is_text_right")
    search_fields = ("type", "title", "menu_title", "content")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("pages",)  # Удобный виджет для выбора страниц

    def get_queryset(self, request):
        """
        Переопределяем queryset для админки.
        Добавляем аннотацию для первой страницы из связанных.
        """
        queryset = super().get_queryset(request)
        # Подзапрос для получения первой страницы (по ID)
        first_page = Page.objects.filter(blocks=OuterRef("pk")).order_by("id")[:1]
        queryset = queryset.annotate(
            first_page_title=Subquery(first_page.values("title"))
        )
        return queryset

    def first_page(self, obj):
        """
        Возвращает название первой страницы, связанной с блоком.
        """
        return obj.first_page_title or "-"

    first_page.short_description = _("Первая страница")


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "meta_title",
        "is_homepage",
        "category",
        "blocks_count",  # Новое поле для отображения количества блоков
    )
    list_filter = ("is_homepage", "category")
    search_fields = ("title", "slug", "meta_title")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [BlockInline]  # Инлайн для блоков

    def blocks_count(self, obj):
        """
        Возвращает количество блоков, связанных со страницей.
        """
        return obj.blocks.count()

    blocks_count.short_description = _("Количество блоков")
    blocks_count.admin_order_field = "blocks__count"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "block",
        "order",
        "alt_text",
        "external_link",
        "link",
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
                    "external_link",
                    "link",
                    "btn_title",
                )
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

    readonly_fields = ("text_rendered",)


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
