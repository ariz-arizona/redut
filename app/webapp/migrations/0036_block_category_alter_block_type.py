# Generated by Django 5.1.7 on 2025-05-01 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0035_alter_block_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blocks', to='webapp.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='block',
            name='type',
            field=models.CharField(choices=[('text', 'Текстовый блок'), ('lead', 'Лид'), ('slider', 'Главная картинка'), ('gallery', 'Карусель'), ('feedback', 'Форма обратной связи'), ('category', 'Вывод категории')], max_length=20, verbose_name='Тип блока'),
        ),
    ]
