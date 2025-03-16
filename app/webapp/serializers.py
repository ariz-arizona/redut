from rest_framework import serializers
from .models import SEO

class SEOSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели SEO.
    """
    class Meta:
        model = SEO
        fields = ['id', 'title', 'meta_description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']  # Эти поля нельзя изменять через API