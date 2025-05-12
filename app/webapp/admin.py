from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db.models import OuterRef, Subquery, Q, CharField, Case, When, Value, F
from django.db.models.functions import Concat
from django.db.models.fields import IntegerField

from server.logger import logger
from .models import (
    Block,
    Category,
    Document,
    Feedback,
    Image,
    Page,
    SiteSettings,
    TopItem,
    ContentBlock,
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


class ContentBlockInline(GenericTabularInline):
    """
    Универсальный инлайн для связи блоков с категориями или страницами.
    """

    model = ContentBlock
    extra = 1
    verbose_name = _("Блок")
    verbose_name_plural = _("Блоки")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Настройка виджета для выбора блоков.
        """
        if db_field.name == "block":
            kwargs["queryset"] = Block.objects.all().order_by("id")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TopItemInline(admin.TabularInline):
    """
    Inline для управления TopItem в админке.
    """

    model = TopItem
    extra = 1  # Количество дополнительных строк для новых элементов
    fields = ("title", "content_block", "order")  # Поля для отображения

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Ограничиваем выбор content_block только активными объектами.
        """
        if db_field.name == "content_block":
            kwargs["queryset"] = ContentBlock.objects.select_related(
                "content_type", "block"
            ).all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
    inlines = [TopItemInline, DocumentInline]

    fieldsets = (
        (
            None,
            {
                "fields": ("name", "phone_number", "logo", "favicon", "is_enabled"),
            },
        ),
        (
            "Футер",
            {
                "fields": ("footer_text_md",),
            },
        ),
    )
    readonly_fields = ("footer_text", "documents_count")

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
    list_display = ("title", "slug", "pages_count")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}  # Автозаполнение slug из title
    inlines = [ContentBlockInline]  # Добавляем инлайн для блоков

    def pages_count(self, obj):
        """
        Возвращает количество страниц в категории.
        """
        return obj.pages.count()

    pages_count.short_description = _("Количество страниц")
    pages_count.admin_order_field = "pages__count"


class RelatedObjectFilter(admin.SimpleListFilter):
    title = _("Связанный объект")  # заголовок фильтра
    parameter_name = "related_object"  # параметр в URL (?related_object=...)

    def lookups(self, request, model_admin):
        """
        Возвращает список доступных вариантов для фильтрации.
        Собираем все Page + Category в формате:
        (type_id:object_id, "Заголовок (slug) | Тип")
        """
        results = []

        # Добавляем страницы
        for page in Page.objects.all():
            key = f"page_{page.id}"
            label = f"{page.title} ({page.slug}) | Страница"
            results.append((key, label))

        # Добавляем категории
        for category in Category.objects.all():
            key = f"category_{category.id}"
            label = f"{category.title} ({category.slug}) | Категория"
            results.append((key, label))

        return results

    def queryset(self, request, queryset):
        """
        Фильтрует Block по выбранному связанному объекту.
        """
        value = self.value()
        if value:
            try:
                content_type_name, obj_id = value.split("_", 1)
                obj_id = int(obj_id)

                if content_type_name == "page":
                    content_type = ContentType.objects.get_for_model(Page)
                elif content_type_name == "category":
                    content_type = ContentType.objects.get_for_model(Category)
                else:
                    return queryset

                return queryset.filter(
                    content_blocks__content_type=content_type,
                    content_blocks__object_id=obj_id,
                )

            except Exception:
                return queryset

        return queryset.distinct()


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "sub_title", "slug", "related_objects")
    list_filter = (
        "type",
        "is_text_right",
        RelatedObjectFilter,
    )
    search_fields = ("type", "title", "content_md")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ImageInline]
    readonly_fields = ("content",)

    def related_objects(self, obj):
        return obj.related_objects

    related_objects.short_description = "Связанные страницы/категории"


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "meta_title",
        "is_homepage",
        "category",
        "blocks_count",  # Количество блоков
    )
    list_filter = ("is_homepage", "category")
    search_fields = ("title", "slug", "meta_title")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ContentBlockInline]  # Добавляем инлайн для блоков

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
