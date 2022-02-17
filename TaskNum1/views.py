from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from TaskNum1.forms import UserCreationForm
from .models import Hotel, UserProfile, HotelPhoto, HotelComment, UsersRatingHotel

choise = {'on': True, None: False}


class HotelPage(View):

    def get(self, request, pk):
        hotel = Hotel.objects.get(pk=pk)
        hotel_photos = HotelPhoto.objects.filter(hotel_id=pk)
        hotel_comments = HotelComment.objects.filter(hotel_id=pk)
        other_user_hotels = Hotel.objects.filter(user=hotel.user).exclude(pk=pk)
        hotel_rating, created = UsersRatingHotel.objects.get_or_create(user_id=request.user.id,
                                                                       hotels=hotel)

        context = {
            'hotel': hotel,
            'hotel_photo': hotel_photos,
            'hotel_comments': hotel_comments,
            'other_user_hotels': other_user_hotels,
            'hotel_rating': hotel_rating,
        }
        return render(request, 'pages/hotel.html', context=context)

    def post(self, request, pk):
        hotel = Hotel.objects.get(pk=pk)
        rating = request.POST.get('rating_ajax')
        user_rating, created = UsersRatingHotel.objects.get_or_create(user_id=request.user.id, hotels=hotel)
        user_rating.rating_from_user_for_hotel = rating
        user_rating.save()
        all_rat = UsersRatingHotel.objects.filter(hotels=hotel)
        get_all_user_ratings = [int(e.rating_from_user_for_hotel) for e in all_rat]
        hotel.star_rating = int(sum(get_all_user_ratings) / (len(get_all_user_ratings)))
        hotel.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PostHotel(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'pages/post_hotel.html')
        return HttpResponseRedirect(reverse('profile'))

    def post(self, request):
        errors = {}
        title = request.POST.get("title")
        breakfast_included = request.POST.get("breakfast")
        room_description = request.POST.get("room_description")
        photos = request.FILES.getlist('photos')
        price_for_room = request.POST.get('price_for_room')
        address = request.POST.get("address")
        if not photos:
            errors['photos'] = "Прикрепите хотябы 1 изображение"
        else:
            hotel = Hotel(title=title, breakfast_included=choise[breakfast_included],
                          room_description=room_description, price_for_room=price_for_room,
                          address=address, user=request.user)
            try:
                hotel.full_clean()
            except ValidationError as err:
                errors = err.message_dict
            else:
                hotel.save()
                for photo in photos:
                    HotelPhoto(hotel=hotel, photo=photo).save()
        if errors: return render(request, 'pages/post_hotel.html', context={'errors': errors})

        return HttpResponseRedirect(reverse('profile'))


class ChangePhotoProfile(View):

    def post(self, request):
        if request.user.is_authenticated:
            photo_profile = request.FILES.get('photo_file')
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.avatar.delete()
            user_profile.avatar = photo_profile
            user_profile.save()
            return HttpResponseRedirect(reverse('profile'))


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = UserCreationForm()

        if request.method == 'POST':
            form = UserCreationForm(request.POST)

            if form.is_valid():
                user = form.save()
                login(request, user)
                return HttpResponseRedirect(reverse('profile'))

        context = {'form': form, "messages": form.errors}

    return render(request, 'registration/register.html', context)


class Profile(View):

    def get(self, request):
        if request.user.is_authenticated:
            user_hotel = Hotel.objects.filter(user=request.user)
            user_profile_photo, created = UserProfile.objects.get_or_create(user=request.user)
            for hotel in user_hotel:
                hotel = Hotel.objects.get(pk=hotel.id)
                hotel.photo = HotelPhoto.objects.filter(hotel_id=hotel.id).values()[0]['photo']
                hotel.save()
            context = {
                'user': request.user,
                'user_profile_photo': user_profile_photo.avatar if user_profile_photo.avatar else None,
                'user_hotels': user_hotel.values(),

            }
            return render(request, 'pages/profile.html', context)
        else:
            return HttpResponseRedirect(reverse('login'))


def login_(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'registration/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


class Home(View):
    def get(self, request):
        user_hotel = Hotel.objects.all()
        context = {
            "user_hotels": user_hotel,
        }
        return render(request, 'pages/hotels.html', context=context)


def delete_hotel(request, pk):
    if request.method == "POST":
        hotel = Hotel.objects.get(pk=pk)
        hotel.delete()
        return HttpResponseRedirect(reverse('profile'))


def add_hotel_comment(request, pk):
    if request.method == "POST":
        user_comment = request.POST.get('comment')
        hotel = Hotel.objects.get(pk=pk)
        HotelComment.objects.create(hotel=hotel, user_comment=user_comment, user=request.user).save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
