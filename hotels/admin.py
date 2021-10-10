from django.contrib import admin

# Register your models here.
from .models import Hotel, Room


class HotelAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['hotelNo', 'name', 'brand']}),
        ('地址信息', {'fields': ['city', 'addr']}),
    ]
    list_display = ('hotelNo', 'name', 'brand', 'city')
    search_fields = ('hotelNo',)
    list_display_links = ('hotelNo', 'name',)
    list_per_page = 20
    list_max_show_all = 200


admin.site.register(Hotel, HotelAdmin)


class RoomAdmin(admin.ModelAdmin):
    fieldsets = [
        ('房间信息', {'fields': ['title', 'hotel', 'roomNo', 'roomType', 'countsBed', 'countsBreakfirst',
            'checkInDate', 'checkOutDate', 'isTwoNightsMore',
                             'countsMember', 'costPrice']}),
        ('代理信息', {'fields': ['agent1', 'agent1Price', 'agent2', 'agent2Price', ]}),
    ]
    list_display = ('title', 'roomType', 'checkInDate', 'checkOutDate', 'countsMember', 'countsBed', 'countsBreakfirst', 'costPrice', 'hotel', 'roomSyncTime')
    list_filter = ('checkInDate', 'checkOutDate', 'hotel')
    search_fields = ('roomType',)
    list_display_links = ('title', 'roomType',)
    list_per_page = 20
    list_max_show_all = 200


admin.site.register(Room, RoomAdmin)
