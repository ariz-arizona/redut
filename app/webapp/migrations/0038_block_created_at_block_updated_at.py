# Generated by Django 5.1.7 on 2025-05-01 10:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0037_alter_block_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Дата и время создания блока.', verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='block',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Дата и время последнего изменения блока.', verbose_name='Дата изменения'),
        ),
    ]
