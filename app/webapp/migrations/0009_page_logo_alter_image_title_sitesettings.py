# Generated by Django 5.1.7 on 2025-03-24 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_block_menu_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='logo',
            field=models.ImageField(blank=True, help_text='Загрузите логотип сайта.', null=True, upload_to='site_logos/', verbose_name='Логотип'),
        ),
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(default='title', max_length=255, verbose_name='Заголовок'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(help_text='Введите номер телефона в международном формате (например, +79991234567).', max_length=20, verbose_name='Номер телефона')),
                ('logo', models.ImageField(blank=True, help_text='Загрузите логотип сайта.', null=True, upload_to='site_logos/', verbose_name='Логотип')),
                ('footer_text', models.TextField(help_text='Введите текст, который будет отображаться в нижней части сайта (футере).', verbose_name='Текст футера')),
                ('is_enabled', models.BooleanField(default=False, help_text='Установите этот флаг, если эта запись должна быть активной. Может быть только одна активная запись.', verbose_name='Активен')),
            ],
            options={
                'verbose_name': 'Настройки сайта',
                'verbose_name_plural': 'Настройки сайта',
                'constraints': [models.UniqueConstraint(condition=models.Q(('is_enabled', True)), fields=('is_enabled',), name='unique_enabled_site_settings')],
            },
        ),
    ]
