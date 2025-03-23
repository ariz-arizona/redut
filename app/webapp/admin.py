from django.contrib import admin
from .models import Page, Block, Image


# Инлайн для изображений
class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

    def get_fields(self, request, obj=None):
        # Динамическое отображение полей в зависимости от типа блока
        if obj and obj.type == "gallery":
            return ("image", "alt_text", "url", "title", "text", "order")
        elif obj and obj.type == "slider":
            return ("image", "alt_text", "order")
        return ()

    def has_add_permission(self, request, obj=None):
        # Разрешаем добавление только для слайдеров и галерей
        return obj is None or obj.type in ["slider", "gallery"]

    def has_change_permission(self, request, obj=None):
        return self.has_add_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_add_permission(request, obj)


# Админка для блоков
@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("type", "order", "title", "menu_title", "slug", "page")
    list_filter = ("type", "page")
    search_fields = ("type", "title", "menu_title", "content")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ImageInline]


# Инлайн для блоков на страницах
class BlockInline(admin.StackedInline):
    model = Block
    extra = 1
    fields = ("type", "order", "title", "menu_title", "slug", "content", "page")
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
