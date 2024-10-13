# Generated by Django 5.1.1 on 2024-10-06 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('windows', '0012_remove_image_description_remove_image_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('window', 'Window'), ('door', 'Door'), ('window door installation', 'Window Door Installation'), ('curtain walling', 'Curtain Walling'), ('office fit out', 'Office Fit Out')], help_text='Specify if it is a window or door', max_length=100),
        ),
    ]
