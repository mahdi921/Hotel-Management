from django.contrib import admin
from .models import Amenity, RoomType, Room, PricingRule

admin.site.register(Amenity)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(PricingRule)
