# Generated by Django 4.0.2 on 2022-02-16 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskNum1', '0014_alter_hotel_photo_alter_hotel_price_for_room_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='title',
            field=models.CharField(max_length=25),
        ),
    ]
