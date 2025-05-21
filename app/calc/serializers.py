from rest_framework import serializers
from .models import Range, AdditionalService, CalculatorData


class RangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Range
        fields = [
            "name",
            "label",
            "min_value",
            "max_value",
            "description",
            "data_type",
            "is_active",
        ]


class AdditionalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalService
        fields = [
            "id",
            "name",
            "label",
            "description",
            "rate_increase",
            "is_active",
        ]


class CalculatorDataSerializer(serializers.ModelSerializer):
    selected_services = AdditionalServiceSerializer(many=True, read_only=True)

    class Meta:
        model = CalculatorData
        fields = "__all__"
