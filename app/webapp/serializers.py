from rest_framework import serializers
from .models import Page, Block, Image, SiteSettings


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=False)
    
    class Meta:
        model = Image
        fields = "__all__"


class BlockSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Block
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    blocks = BlockSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = "__all__"

class SiteSettingsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели SiteSettings.
    """
    class Meta:
        model = SiteSettings
        fields = '__all__'