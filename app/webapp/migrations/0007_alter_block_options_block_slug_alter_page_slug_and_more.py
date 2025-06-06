# Generated by Django 5.1.7 on 2025-03-23 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_block_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='block',
            options={'ordering': ['page', 'order'], 'verbose_name': 'Блок', 'verbose_name_plural': 'Блоки'},
        ),
        migrations.AddField(
            model_name='block',
            name='slug',
            field=models.SlugField(default='slider', verbose_name='Slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug'),
        ),
        migrations.AddConstraint(
            model_name='block',
            constraint=models.UniqueConstraint(fields=('page', 'slug'), name='unique_slug_per_page'),
        ),
    ]
