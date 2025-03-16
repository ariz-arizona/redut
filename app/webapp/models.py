from django.db import models

class SEO(models.Model):
    """
    Модель для хранения SEO данных.
    """
    title = models.CharField(max_length=255, verbose_name="Title")
    meta_description = models.TextField(verbose_name="Meta Description", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "SEO"
        verbose_name_plural = "SEO"