# Generated by Django 4.0.2 on 2022-02-16 19:03

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('TaskNum1', '0029_alter_hotel_price_for_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='price_for_room',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(flags=re.RegexFlag['IGNORECASE'], inverse_match=True, message='Введен не верный формат цены', regex='\\w')]),
        ),
    ]
