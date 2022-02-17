from .models import Hotel, UserProfile, TestFile, HotelPhoto, HotelComment, UsersRatingHotel
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


# Перерегистрируем модель User

class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Доп. информация'


# Определяем новый класс настроек для модели User
class UserAdmin(UserAdmin):
    inlines = (UserInline,)


admin.site.register(User, UserAdmin)
admin.site.register(Hotel)
admin.site.register(TestFile)
admin.site.register(HotelPhoto)
admin.site.register(HotelComment)
admin.site.register(UsersRatingHotel)
