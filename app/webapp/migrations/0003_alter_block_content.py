# Generated by Django 5.1.7 on 2025-03-22 16:35

import markdownx.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_block_page_delete_seo_page_only_one_homepage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='content',
            field=markdownx.models.MarkdownxField(blank=True, null=True, verbose_name='Контент (Markdown)'),
        ),
    ]
