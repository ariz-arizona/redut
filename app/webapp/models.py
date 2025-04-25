from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from django.utils.translation import gettext_lazy as _

from markdownfield.models import MarkdownField
from markdownfield.validators import VALIDATOR_STANDARD

class TopItem(models.Model):
    """
    Промежуточная модель для хранения ссылок на блоки на страницах или категориях.
    """
    site_settings = models.ForeignKey(
        "SiteSettings",
        on_delete=models.CASCADE,
        related_name="top_items",
        verbose_name="Настройки сайта",
    )

    # Связь с блоком на странице
    page_block = models.ForeignKey(
        "PageBlock",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="top_items",
        verbose_name="Блок на странице",
    )

    # Связь с блоком на категории
    category_block = models.ForeignKey(
        "CategoryBlock",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="top_items",
        verbose_name="Блок на категории",
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Заголовок",
        help_text="Необязательный заголовок. Если не указан, используется название страницы или категории."
    )

    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order"]
        verbose_name = "Top Item"
        verbose_name_plural = "Top Items"

    def clean(self):
        """
        Проверяет, что выбран только один из вариантов: блок на странице или блок на категории.
        """
        if self.page_block and self.category_block:
            raise ValidationError("Можно выбрать либо блок на странице, либо блок на категории, но не оба.")
        if not self.page_block and not self.category_block:
            raise ValidationError("Необходимо выбрать блок на странице или блок на категории.")

    def get_title(self):
        """
        Возвращает заголовок TopItem.
        Если title не указан, использует название страницы или категории.
        """
        if self.title:
            return self.title
        if self.page_block:
            return self.page_block.page.title
        elif self.category_block:
            return self.category_block.category.title
        return "Несвязанный TopItem"

    def __str__(self):
        return f"{self.get_title()} (Order: {self.order})"


class SiteSettings(models.Model):
    """
    Модель для хранения общих сведений о сайте.
    """

    name = models.CharField(max_length=255)
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
    footer_text_md = MarkdownField(
        blank=True,
        null=True,
        validator=VALIDATOR_STANDARD,
        verbose_name="Текст футера",
        help_text="Введите текст, который будет отображаться в нижней части сайта (футере).",
        rendered_field="footer_text",
    )
    footer_text = models.TextField(blank=True, null=True, editable=False)
    is_enabled = models.BooleanField(
        default=False,
        verbose_name="Активен",
        help_text=(
            "Установите этот флаг, если эта запись должна быть активной. "
            "Может быть только одна активная запись."
        ),
    )

    def documents_count(self):
        """
        Возвращает количество документов, связанных с этой записью настроек.
        """
        return self.documents.count()

    documents_count.short_description = _("Количество документов")

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
            enabled_settings = SiteSettings.objects.filter(is_enabled=True)
            if self.pk:
                enabled_settings = enabled_settings.exclude(pk=self.pk)
            if enabled_settings.exists():
                raise ValidationError(
                    "Может быть только одна активная запись настроек сайта."
                )


class Document(models.Model):
    """
    Модель для хранения документов, связанных с настройками сайта.
    """

    title = models.CharField(
        max_length=255,
        verbose_name=_("Название документа"),
        help_text=_("Введите название документа."),
    )
    file = models.FileField(
        upload_to="documents/",
        verbose_name=_("Файл документа"),
        help_text=_("Загрузите файл документа."),
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "docx", "txt"])],
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Описание"),
        help_text=_("Введите описание документа (необязательно)."),
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата загрузки"),
        help_text=_("Дата и время загрузки документа."),
    )
    site_settings = models.ManyToManyField(
        SiteSettings,
        related_name="documents",
        verbose_name=_("Настройки сайта"),
        help_text=_("Выберите настройки сайта, к которым относится этот документ."),
        blank=True,
    )

    class Meta:
        verbose_name = _("Документ")
        verbose_name_plural = _("Документы")
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    Модель для категорий страниц.
    """

    title = models.CharField(
        max_length=255,
        verbose_name=_("Заголовок"),
        help_text=_("Введите заголовок категории."),
    )
    sub_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Подзаголовок"),
        help_text=_("Введите подзаголовок категории (необязательно)."),
    )
    slug = models.SlugField(
        unique=True,
        verbose_name=_("Slug"),
        help_text=_("Уникальный идентификатор категории для URL."),
    )
    blocks = models.ManyToManyField(
        "Block",
        through="CategoryBlock",  # Указываем промежуточную модель
        related_name="categories",
        blank=True,
        verbose_name="Блоки",
        help_text="Выберите блоки, которые будут отображаться на этой странице.",
    )

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ["title"]

    def __str__(self):
        return self.title


class CategoryBlock(models.Model):
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="category_blocks",
        verbose_name="Категория",
    )
    block = models.ForeignKey(
        "Block",
        on_delete=models.CASCADE,
        related_name="block_categories",
        verbose_name="Блок",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order"]  # Сортировка по полю order
        unique_together = ("category", "block")  # Уникальность связи

    def __str__(self):
        return f"Category {self.category.title} - Block {self.block.title} (Order: {self.order})"


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
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="pages",
        verbose_name=_("Категория"),
        help_text=_("Выберите категорию для страницы (необязательно)."),
        blank=True,
        null=True,
    )
    blocks = models.ManyToManyField(
        "Block",
        through="PageBlock",  # Указываем промежуточную модель
        related_name="pages",
        blank=True,
        verbose_name="Блоки",
        help_text="Выберите блоки, которые будут отображаться на этой странице.",
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


class PageBlock(models.Model):
    page = models.ForeignKey(
        "Page",
        on_delete=models.CASCADE,
        related_name="page_blocks",
        verbose_name="Страница",
    )
    block = models.ForeignKey(
        "Block",
        on_delete=models.CASCADE,
        related_name="block_pages",
        verbose_name="Блок",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order"]  # Сортировка по полю order
        unique_together = ("page", "block")  # Уникальность связи

    def __str__(self):
        return (
            f"Page {self.page.title} - Block {self.block.title[:20]} (Order: {self.order})"
        )


class Block(models.Model):
    BLOCK_TYPES = [
        ("text", "Текстовый блок"),
        ("lead", "Лид"),
        ("slider", "Главная картинка"),
        ("gallery", "Карусель"),
        ("feedback", "Форма обратной связи"),
    ]
    type = models.CharField(
        choices=BLOCK_TYPES, max_length=20, verbose_name="Тип блока"
    )
    title = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Заголовок"
    )
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
        verbose_name="Внешняя ссылка",
    )
    btn_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Текст кнопки",
        help_text="Введите текст для кнопки (необязательно).",
    )
    content_md = MarkdownField(
        blank=True,
        null=True,
        validator=VALIDATOR_STANDARD,
        rendered_field="content",
        verbose_name="Контент (Markdown)",
    )
    content = models.TextField(blank=True, null=True, editable=False)
    is_text_right = models.BooleanField(
        default=False,
        verbose_name="Текст справа",
        help_text="Если выбрано, текст будет расположен справа. Иначе — слева.",
    )

    def __str__(self):
        return f"{self.get_type_display()} {self.title}"

    class Meta:
        ordering = ["block_pages__order"]
        verbose_name = "Блок"
        verbose_name_plural = "Блоки"


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
    external_link = models.URLField(blank=True, null=True, verbose_name="Ссылка")
    link = models.ForeignKey(
        "Page",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Внутренняя ссылка",
    )
    btn_title = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Текст кнопки"
    )
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    text = MarkdownField(
        blank=True,
        null=True,
        validator=VALIDATOR_STANDARD,
        rendered_field="text_rendered",
        verbose_name="Текст (Markdown)",
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


class Feedback(models.Model):
    """
    Модель для хранения обратной связи от пользователей.
    """

    name = models.CharField(
        max_length=255,
        verbose_name="Имя",
        help_text="Введите имя отправителя.",
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон",
        help_text="Введите номер телефона в международном формате (например, +79991234567).",
    )
    message = models.TextField(
        blank=True,
        null=True,
        verbose_name="Сообщение",
        help_text="Введите текст сообщения (опционально).",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время создания записи.",
    )

    def __str__(self):
        return f"Feedback from {self.name} ({self.phone})"

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"
        ordering = ["-created_at"]
