# Generated by Django 4.0.2 on 2022-02-15 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TaskNum1', '0004_alter_usersratinghotel_rating_from_user_for_hotel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='overall_rating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TaskNum1.usersratinghotel'),
        ),
    ]
