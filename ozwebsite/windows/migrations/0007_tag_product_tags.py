# Generated by Django 5.1.1 on 2024-10-02 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('windows', '0006_remove_order_tags_delete_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(to='windows.tag'),
        ),
    ]
