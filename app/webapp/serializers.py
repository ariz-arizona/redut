from rest_framework import serializers
from .models import (
    Block,
    Category,
    Document,
    Feedback,
    Image,
    Page,
    SiteSettings,
    TopItem,
)
from server.logger import logger


class DocumentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Document.
    """

    file = serializers.FileField(use_url=False)

    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "file",  # URL файла будет автоматически сгенерирован через FileField
            "description",
            "uploaded_at",
        ]


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=False)
    link = serializers.SlugRelatedField(
        slug_field="slug",  # Указываем, что нужно использовать поле slug
        queryset=Page.objects.all(),  # Queryset для поля ForeignKey
        allow_null=True,  # Разрешаем null значения
        required=False,  # Поле необязательное
    )

    class Meta:
        model = Image
        fields = "__all__"


class BlockSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    
    link = serializers.SlugRelatedField(
        slug_field="slug",  # Указываем, что нужно использовать поле slug
        queryset=Page.objects.all(),  # Queryset для поля ForeignKey
        allow_null=True,  # Разрешаем null значения
        required=False,  # Поле необязательное
    )

    class Meta:
        model = Block
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    blocks = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = "__all__"
        
    def get_blocks(self, obj):
        blocks = obj.get_blocks()
        return BlockSerializer(blocks, many=True).data


class CategorySerializer(serializers.ModelSerializer):
    blocks = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"
        
    def get_blocks(self, obj):
        blocks = obj.get_blocks()
        return BlockSerializer(blocks, many=True).data

class TopItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели TopItem.
    """
    type = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    block = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = TopItem
        fields = ["id", "type", "slug", "block", "title", "order"]

    def get_type(self, obj):
        """
        Возвращает тип элемента: 'page' или 'category'.
        """
        content_object = obj.content_block.content_object
        if isinstance(content_object, Page):
            return "page"
        elif isinstance(content_object, Category):
            return "category"
        return None

    def get_slug(self, obj):
        """
        Возвращает slug страницы или категории.
        """
        content_object = obj.content_block.content_object
        if isinstance(content_object, Page):
            # Если это главная страница, возвращаем пустую строку
            return "" if content_object.is_homepage else content_object.slug
        elif isinstance(content_object, Category):
            return content_object.slug
        return None

    def get_block(self, obj):
        """
        Возвращает slug блока.
        """
        return obj.content_block.block.slug

    def get_title(self, obj):
        """
        Возвращает заголовок TopItem.
        Если title не указан, используется название страницы или категории.
        """
        if obj.title:
            return obj.title
        content_object = obj.content_block.content_object
        return getattr(content_object, "title", "Несвязанный TopItem")

class SiteSettingsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели SiteSettings.
    """

    logo = serializers.FileField(use_url=False)
    documents = DocumentSerializer(many=True, read_only=True)
    top_items = TopItemSerializer(many=True, read_only=True)

    class Meta:
        model = SiteSettings
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "name", "phone", "message", "created_at"]
        read_only_fields = ["created_at"]  # Поле `created_at` только для чтения
