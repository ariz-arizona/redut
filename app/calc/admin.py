from django.contrib import admin
from .models import Range, AdditionalService, CalculatorData, BaseRate

# -------------------------------
# Админка для модели Range
# -------------------------------


@admin.register(Range)
class RangeAdmin(admin.ModelAdmin):
    list_display = ("name", "min_value", "max_value", "data_type", "is_active")
    list_filter = ("data_type", "is_active")
    search_fields = ("name", "description")
    fieldsets = (
        (None, {"fields": ("name", "label", "is_active")}),
        ("Диапазон значений", {"fields": ("min_value", "max_value")}),
        (
            "Дополнительно",
            {"fields": ("description", "data_type"), "classes": ("collapse",)},
        ),
    )
    ordering = ("name",)
    save_on_top = True


# -------------------------------
# Админка для модели AdditionalService
# -------------------------------


@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "rate_increase", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    fields = ("name", "label", "description", "rate_increase", "is_active")
    ordering = ("name",)
    save_on_top = True


@admin.register(BaseRate)
class BaseRateAdmin(admin.ModelAdmin):
    list_display = ("rate",)


# -------------------------------
# Админка для модели CalculatorData
# -------------------------------


@admin.register(CalculatorData)
class CalculatorDataAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "property_cost",
        "initial_payment_percent",
        "loan_term_years",
        "use_maternity_capital",
        "created_at",
    )
    list_filter = ("use_maternity_capital", "created_at")
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("selected_services",)
    fieldsets = (
        (
            "Основные параметры",
            {
                "fields": (
                    "property_cost",
                    "initial_payment_percent",
                    "loan_term_years",
                    "use_maternity_capital",
                )
            },
        ),
        ("Дополнительные услуги", {"fields": ("selected_services",)}),
        (
            "Статус и дата",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
    ordering = ("-created_at",)
    save_on_top = True
