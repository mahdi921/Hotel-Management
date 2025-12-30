from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest', 'room', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'check_in')
    search_fields = ('guest__username', 'room__room_number')
