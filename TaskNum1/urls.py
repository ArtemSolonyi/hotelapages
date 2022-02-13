from django.urls import path
from TaskNum1.views import login_, Register, Home, Profile, PostHotel, ChangePhotoProfile, HotelPage
from TaskNum1 import views

urlpatterns = [
    path('login', login_, ),
    path('register', Register.as_view(), name='register'),
    path('', Home.as_view(), name='home'),
    path('profile', Profile.as_view(), name='profile'),
    path('post_hotel', PostHotel.as_view(), name='post_hotel'),
    path('change_photo', ChangePhotoProfile.as_view(), name='change_photo_profile'),
    path('delete_hotel/<str:pk>/', views.delete_hotel, name='delete_hotel'),
    path(r'hotel/<str:pk>', HotelPage.as_view(), name='hotel'),
    path('comment/<str:pk>', views.add_hotel_comment, name='hotel_comment'),
]
