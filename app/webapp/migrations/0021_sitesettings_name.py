# Generated by Django 5.1.6 on 2025-04-22 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0020_alter_sitesettings_footer_text_md'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='name',
            field=models.CharField(default='REDUT', max_length=255),
            preserve_default=False,
        ),
    ]
