from rest_framework import serializers
from .models import Page, Block, Image, SiteSettings, Feedback, Document, Category


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
    blocks = BlockSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class SiteSettingsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели SiteSettings.
    """

    logo = serializers.FileField(use_url=False)
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = SiteSettings
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "name", "phone", "message", "created_at"]
        read_only_fields = ["created_at"]  # Поле `created_at` только для чтения
