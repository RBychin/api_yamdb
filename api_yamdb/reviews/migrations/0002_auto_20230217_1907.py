# Generated by Django 3.2 on 2023-02-17 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(verbose_name='Краткое имя категории'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(verbose_name='Краткое имя жанра'),
        ),
    ]
