# Generated by Django 5.1.7 on 2025-05-01 10:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0038_block_created_at_block_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='favicon',
            field=models.FileField(blank=True, help_text='Загрузите favicon сайта.', null=True, upload_to='favicon/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])], verbose_name='favicon'),
        ),
    ]
