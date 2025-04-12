from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from markdownfield.models import MarkdownField
from markdownfield.validators import VALIDATOR_STANDARD


class SiteSettings(models.Model):
    """
    Модель для хранения общих сведений о сайте.
    """

    phone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона в международном формате (например, +79991234567).",
    )

    logo = models.FileField(
        upload_to="site_logos/",
        verbose_name="Логотип",
        help_text="Загрузите логотип сайта.",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "svg"])
        ],
    )

    footer_text = models.TextField(
        verbose_name="Текст футера",
        help_text="Введите текст, который будет отображаться в нижней части сайта (футере).",
    )

    is_enabled = models.BooleanField(
        default=False,
        verbose_name="Активен",
        help_text=(
            "Установите этот флаг, если эта запись должна быть активной. "
            "Может быть только одна активная запись."
        ),
    )

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"
        constraints = [
            models.UniqueConstraint(
                fields=["is_enabled"],
                condition=models.Q(is_enabled=True),
                name="unique_enabled_site_settings",
            )
        ]

    def __str__(self):
        return "Общие настройки сайта"

    @staticmethod
    def get_enabled():
        """
        Возвращает активную запись настроек сайта (где is_enabled=True).
        Если активной записи нет, возвращает None.
        """
        return SiteSettings.objects.filter(is_enabled=True).first()

    def clean(self):
        """
        Проверяет, что только одна запись может быть активной (is_enabled=True).
        """
        if self.is_enabled:
            # Ищем другие активные записи, исключая текущую
            enabled_settings = SiteSettings.objects.filter(is_enabled=True)
            if self.pk:
                enabled_settings = enabled_settings.exclude(pk=self.pk)
            if enabled_settings.exists():
                raise ValidationError(
                    "Может быть только одна активная запись настроек сайта."
                )


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
    logo = models.ImageField(
        upload_to="site_logos/",
        verbose_name="Логотип",
        help_text="Загрузите логотип сайта.",
        blank=True,
        null=True,
    )

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
        ("text_right", "Текст справа"),
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
    sub_title = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Подзаголовок"
    )
    slug = models.SlugField(verbose_name="Slug")
    link = models.ForeignKey(
        "Page",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Внутренняя ссылка",
    )
    external_link = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Внешняяы ссылка",
    )
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
        return f"{self.get_type_display()} {self.title} (Order: {self.order})"

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
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    text = MarkdownField(
        blank=True,
        null=True,
        validator=VALIDATOR_STANDARD,  # Валидатор для Markdown
        rendered_field="text_rendered",  # Поле для хранения HTML
        verbose_name="Контент (Markdown)",
    )
    text_rendered = models.TextField(blank=True, null=True, editable=False)
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    def __str__(self):
        if self.block:
            return f"Image for {self.block.type} (Order: {self.order})"
        return f"Unlinked Image (Order: {self.order})"

    class Meta:
        ordering = ["order"]
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
