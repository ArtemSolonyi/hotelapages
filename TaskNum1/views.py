from django.contrib.auth import authenticate, login
from TaskNum1.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from .models import Hotel, UserProfile, User, HotelPhoto, HotelComment

choise = {'on': True, None: False}


class HotelPage(View):
    def get(self, request, pk):
        hotel = Hotel.objects.get(pk=pk)
        hotel_photos = HotelPhoto.objects.filter(hotel_id=pk)
        hotel_comments = HotelComment.objects.filter(hotel_id=pk)
        other_user_hotels = Hotel.objects.filter(user=hotel.user).exclude(pk=pk)
        context = {
            'hotel': hotel,
            'hotel_photo': hotel_photos,
            'hotel_comments': hotel_comments,
            'other_user_hotels': other_user_hotels,

        }
        return render(request, 'pages/hotel.html', context=context)


class PostHotel(View):
    def get(self, request):
        return render(request, 'pages/post_hotel.html')

    def post(self, request):
        title = request.POST.get("title")
        breakfast_included = request.POST.get("breakfast")
        room_description = request.POST.get("room_description")
        photos = request.FILES.getlist('photos')
        price_for_room = request.POST.get('price_for_room')
        address = request.POST.get("address")
        star_rating = request.POST.get('rating')
        hotel = Hotel.objects.create(title=title, breakfast_included=choise[breakfast_included],
                                     room_description=room_description, price_for_room=price_for_room,
                                     address=address, user=request.user, star_rating=star_rating)
        for photo in photos:
            HotelPhoto(hotel=hotel, photo=photo).save()
        return render(request, 'pages/profile.html')


class ChangePhotoProfile(View):
    def post(self, request):
        photo_profile = request.FILES.get('photo_file')
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            try:
                user_profile = UserProfile.objects.get(user=user)
                user_profile.avatar.delete()
                user_profile.avatar = photo_profile
                user_profile.save()
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create(user=user, avatar=photo_profile)
                user_profile.save()
            return HttpResponseRedirect(reverse('profile'))

    def get(self, request):
        return render(request, 'pages/profile.html')


class Register(View):

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, 'registration/register.html', context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            authenticate(email=email, password=password)
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        context = {
            'form': form
        }
        return render(request, 'registration/register.html', context)


class Profile(View):
    def get(self, request):
        user_profile_photo = None
        user_hotel = Hotel.objects.filter(user=request.user)
        if request.user.is_authenticated:
            try:
                user_profile_photo = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=request.user)

        for hotel in user_hotel:
            hotel = Hotel.objects.get(pk=hotel.id)
            hotel.photo = HotelPhoto.objects.filter(hotel_id=hotel.id).values()[0]['photo']
            hotel.save()

        context = {
            'user': request.user,
            'user_profile_photo': user_profile_photo.avatar if request.user.is_authenticated else None,
            'user_hotels': user_hotel.values() if request.user.is_authenticated else None,

        }
        return render(request, 'pages/profile.html', context)


def login_(request):
    return render(request, 'registration/login.html')


def logout(request):
    return render(request, '')


class Home(View):
    def get(self, request):
        return render(request, 'pages/navbar.html', )


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
