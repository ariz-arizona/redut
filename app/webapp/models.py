from django.db import models
from django.core.exceptions import ValidationError

from markdownfield.models import MarkdownField
from markdownfield.validators import VALIDATOR_STANDARD


class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    meta_title = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Meta Title"
    )
    meta_description = models.TextField(
        blank=True, null=True, verbose_name="Meta Description"
    )
    is_homepage = models.BooleanField(default=False, verbose_name="Главная страница")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        constraints = [
            models.UniqueConstraint(
                fields=["is_homepage"],
                condition=models.Q(is_homepage=True),
                name="only_one_homepage",
            )
        ]


class Block(models.Model):
    BLOCK_TYPES = [
        ("text", "Текстовый блок"),
        ("slider", "Слайдер"),
        ("gallery", "Галерея"),
    ]

    page = models.ForeignKey(
        "Page",
        related_name="blocks",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Страница",
    )
    type = models.CharField(
        choices=BLOCK_TYPES, max_length=20, verbose_name="Тип блока"
    )
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="Slug")
    menu_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Заголовок меню",
        help_text="Необязательное поле. Если указано, будет использоваться в меню вместо основного заголовка.",
    )
    order = models.PositiveIntegerField(verbose_name="Порядок")
    content = MarkdownField(
        blank=True,
        null=True,
        validator=VALIDATOR_STANDARD,  # Валидатор для Markdown
        rendered_field="content_rendered",  # Поле для хранения HTML
        verbose_name="Контент (Markdown)",
    )
    content_rendered = models.TextField(blank=True, null=True, editable=False)

    def __str__(self):
        return f"{self.get_type_display()} (Order: {self.order})"

    class Meta:
        ordering = ["page", "order"]
        verbose_name = "Блок"
        verbose_name_plural = "Блоки"
        constraints = [
            models.UniqueConstraint(
                fields=["page", "slug"],
                name="unique_slug_per_page",
            ),
        ]


class Image(models.Model):
    block = models.ForeignKey(
        "Block",
        related_name="images",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Блок",
    )
    image = models.ImageField(upload_to="block_images/", verbose_name="Изображение")
    alt_text = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Альтернативный текст"
    )
    url = models.URLField(blank=True, null=True, verbose_name="Ссылка (для галереи)")
    title = models.CharField(
        max_length=255,  verbose_name="Заголовок"
    )
    text = models.TextField(
        blank=True, null=True, verbose_name="Описание (для галереи)"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    def __str__(self):
        if self.block:
            return f"Image for {self.block.type} (Order: {self.order})"
        return f"Unlinked Image (Order: {self.order})"

    class Meta:
        ordering = ["order"]
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
