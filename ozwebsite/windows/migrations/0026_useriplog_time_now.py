# Generated by Django 5.1.1 on 2024-10-12 00:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('windows', '0025_useriplog_page_visited'),
    ]

    operations = [
        migrations.AddField(
            model_name='useriplog',
            name='time_now',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
