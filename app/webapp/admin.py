from django.contrib import admin
from .models import Page, Block, Image


# Инлайн для изображений
class ImageInline(admin.StackedInline):
    model = Image
    extra = 1

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
