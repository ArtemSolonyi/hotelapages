# Generated by Django 4.0.2 on 2022-02-15 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskNum1', '0006_usersratinghotel_hotels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, default=None, upload_to='images/'),
        ),
    ]
