# Generated by Django 4.0.2 on 2022-02-16 15:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskNum1', '0021_alter_hotel_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='room_description',
            field=models.TextField(validators=[django.core.validators.MaxLengthValidator(limit_value=100, message='Описание слишком большое,максимально количество слов 100'), django.core.validators.MinValueValidator(limit_value=20, message='Минимальное количество слов описания, 20')]),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='title',
            field=models.CharField(max_length=50, validators=[django.core.validators.MaxLengthValidator(limit_value=50, message='Название слишком большое')]),
        ),
    ]