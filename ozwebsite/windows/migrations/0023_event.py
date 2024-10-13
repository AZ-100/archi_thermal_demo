# Generated by Django 5.1.1 on 2024-10-11 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('windows', '0022_quoterequest_address_quoterequest_suburb'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
    ]
