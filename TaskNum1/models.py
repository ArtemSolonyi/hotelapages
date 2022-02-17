from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import *
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
    )
    profile = models.ForeignKey("TaskNum1.UserProfile", on_delete=models.CASCADE, null=True, blank=True,
                                related_name="+")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, unique=True)
    avatar = models.ImageField(blank=True, default=None, upload_to='images/')

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def get_avatar_url(self):
        return f"{self.avatar}"


class TestFile(models.Model):
    file = models.ImageField(blank=True, null=True, upload_to='images/',
                             validators=[MinLengthValidator(limit_value=1, message="Прикрепите хотябы 1 изображение")])


class Hotel(models.Model):
    title = models.TextField(validators=[MaxLengthValidator(
        limit_value=50,
        message="Название слишком большое"
    )])
    star_rating = models.IntegerField(default=0, blank=True, null=True)
    breakfast_included = models.BooleanField(default=False)
    photo = models.ImageField(blank=True, null=True, upload_to='images/', )
    room_description = models.TextField(validators=[MaxLengthValidator(
        limit_value=100,
        message="Описание слишком большое,максимально количество слов 100"
    )])
    price_for_room = models.TextField(blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^[-+]?[0-9]+$',
            message="Неверный формат введенной цены",
            inverse_match=False,
        )])
    address = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_photo_path(self):
        return f"{self.photo}"


class HotelPhoto(models.Model):
    photo = models.ImageField(blank=True, null=True, upload_to='images/')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='photos')


class HotelComment(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_comment = models.TextField()
    date = models.DateTimeField(default=datetime.now, blank=True)


class UsersRatingHotel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    hotels = models.ForeignKey(Hotel, on_delete=models.CASCADE, default=None)
    rating_from_user_for_hotel = models.CharField(null=True, blank=True, max_length=1)
