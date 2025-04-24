from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Page, Block, Image, SiteSettings, Feedback, Document, Category


class DocumentInline(admin.TabularInline):
    """
    Inline для отображения документов в админке SiteSettings.
    """

    model = Document.site_settings.through
    extra = 1
    verbose_name = _("Документ")
    verbose_name_plural = _("Документы")


# Инлайн для изображений
class ImageInline(admin.StackedInline):
    model = Image
    extra = 1
    classes = ["collapse"]  # Сворачиваем весь инлайн

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
                    "slug",
                    "sub_title",
                    "btn_title",
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
                "fields": ("content",),
            },
        ),
    )


class PageInline(admin.TabularInline):
    """
    Inline для отображения страниц в админке категории.
    """

    model = Page
    extra = 0
    fields = ("title", "slug", "is_homepage")  # Отображаемые поля
    readonly_fields = ("slug",)  # Slug только для чтения
    show_change_link = True  # Позволяет переходить к редактированию страницы


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "sub_title", "slug", "pages_count")
    search_fields = ("title", "sub_title")
    prepopulated_fields = {"slug": ("title",)}  # Автозаполнение slug из title
    inlines = [PageInline]

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
                    "btn_title",
                    "order",
                    "is_text_right",  # Поле для текста справа/слева
                ),
            },
        ),
        (
            "Привязка к странице",
            {
                "fields": ("page",),
            },
        ),
        (
            "Ссылки",
            {
                "fields": (
                    "link",
                    "external_link",
                ),
                "classes": ["collapse"],  # Добавляем класс 'collapse'
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
                "classes": ["collapse"],  # Добавляем класс 'collapse'
            },
        ),
    )

    readonly_fields = (
        "content_rendered",
    )  # Делаем отрендеренный контент только для чтения


class PageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "meta_title",
        "is_homepage",
        "category",
    )
    list_filter = ("is_homepage", "category")  # Фильтр по категории
    search_fields = ("title", "slug", "meta_title")
    prepopulated_fields = {"slug": ("title",)}  # Автозаполнение slug из title
    inlines = [BlockInline]  # Добавляем инлайн для блоков

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "title",
                    "slug",
                    "meta_title",
                    "meta_description",
                ),
            },
        ),
        (
            "Настройки",
            {
                "fields": (
                    "is_homepage",
                    "logo",
                    "category",
                ),
            },
        ),
    )


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

    readonly_fields = (
        "text_rendered",
    )  # Делаем отрендеренный контент только для чтения


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Админка для модели SiteSettings.
    """

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
