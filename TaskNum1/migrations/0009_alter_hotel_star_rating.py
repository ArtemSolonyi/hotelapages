# Generated by Django 4.0.2 on 2022-02-15 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskNum1', '0008_alter_usersratinghotel_hotels_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='star_rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
