from django.contrib import admin
from .models import HousekeepingTask

@admin.register(HousekeepingTask)
class HousekeepingTaskAdmin(admin.ModelAdmin):
    list_display = ('room', 'assigned_to', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('room__room_number', 'assigned_to__username')
