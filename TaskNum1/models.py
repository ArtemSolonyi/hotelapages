from datetime import datetime

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models


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
    avatar = models.ImageField(blank=True, null=True, upload_to='images/')

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class TestFile(models.Model):
    file = models.ImageField(blank=True, null=True, upload_to='images/')


class Hotel(models.Model):
    title = models.CharField(max_length=200)
    star_rating = models.TextField()
    breakfast_included = models.BooleanField(default=False)
    photo = models.ImageField(blank=True, null=True, upload_to='images/')
    room_description = models.TextField()
    price_for_room = models.TextField()
    address = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class HotelPhoto(models.Model):
    photo = models.ImageField(blank=True, null=True, upload_to='images/')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='photos')


class HotelComment(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_comment = models.TextField()
    date = models.DateTimeField(default=datetime.now, blank=True)
