from django.shortcuts import render
from .models import Hotel, Room
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def hotels(request):
    hotel_list = Hotel.objects.all().order_by('id')
    paginator = Paginator(hotel_list, 10)  # Show 25 contacts per page

    page = request.GET.get('page', 1)
    try:
        hotels = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        hotels = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        hotels = paginator.page(paginator.num_pages)

    return render(request, 'hotels.html', {'hotels': hotels})


def rooms(request):
    page = request.GET.get('page', 1)
    hotelno = request.GET.get('hotelno')
    room_list = Room.objects.filter(hotel=hotelno).order_by('id')
    paginator = Paginator(room_list, 10)  # Show 25 contacts per page
    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        rooms = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        rooms = paginator.page(paginator.num_pages)

    return render(request, 'rooms.html', {'rooms': rooms, 'hotelno': hotelno})
