# Generated by Django 4.0.2 on 2022-02-15 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TaskNum1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='star_rating',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='UsersRatingHotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_from_user_for_hotel', models.IntegerField(blank=True, null=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TaskNum1.hotel')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='user_rating_for_hotel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='TaskNum1.usersratinghotel'),
        ),
    ]
