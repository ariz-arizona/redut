from django.db import models


class Range(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100)
    label = models.CharField(verbose_name="Ключ", max_length=100, blank=True, null=True)

    min_value = models.DecimalField(
        verbose_name="Минимальное значение", max_digits=12, decimal_places=2
    )
    max_value = models.DecimalField(
        verbose_name="Максимальное значение", max_digits=12, decimal_places=2
    )
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    data_type = models.CharField(
        verbose_name="Тип данных",
        max_length=20,
        choices=[
            ("decimal", "Decimal"),
            ("integer", "Integer"),
            ("percent", "Percent"),
        ],
        default="decimal",
    )
    is_active = models.BooleanField(verbose_name="Активно", default=True)

    class Meta:
        verbose_name = "Диапазон"
        verbose_name_plural = "Диапазоны"

    def __str__(self):
        return self.name


class AdditionalService(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    label =models.CharField(verbose_name="Ключ", max_length=100, blank=True, null=True)
    
    description = models.TextField(verbose_name="Описание")
    rate_increase = models.DecimalField(
        verbose_name="Изменение ставки (%)",
        max_digits=5,
        decimal_places=2,
        help_text="Процент изменения ставки при подключении услуги",
    )
    is_active = models.BooleanField(verbose_name="Активно", default=True)

    class Meta:
        verbose_name = "Дополнительная услуга"
        verbose_name_plural = "Дополнительные услуги"

    def __str__(self):
        return self.name


class CalculatorData(models.Model):
    property_cost = models.DecimalField(
        verbose_name="Стоимость недвижимости", max_digits=12, decimal_places=2
    )
    initial_payment_percent = models.DecimalField(
        verbose_name="Первоначальный взнос (%)", max_digits=5, decimal_places=2
    )
    loan_term_years = models.PositiveIntegerField(verbose_name="Срок кредита (лет)")
    use_maternity_capital = models.BooleanField(
        verbose_name="Использовать материнский капитал", default=False
    )
    selected_services = models.ManyToManyField(
        AdditionalService, verbose_name="Выбранные услуги", blank=True
    )

    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name="Дата последнего обновления", auto_now=True
    )

    class Meta:
        verbose_name = "Расчёт калькулятора"
        verbose_name_plural = "Расчёты калькулятора"

    def __str__(self):
        return f"Расчет #{self.id}"
