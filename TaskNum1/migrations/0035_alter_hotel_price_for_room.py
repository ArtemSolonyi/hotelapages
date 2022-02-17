# Generated by Django 4.0.2 on 2022-02-16 19:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskNum1', '0034_alter_hotel_price_for_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='price_for_room',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(inverse_match=False, message='vs', regex='^[-+]?[0-9]+$')]),
        ),
    ]
