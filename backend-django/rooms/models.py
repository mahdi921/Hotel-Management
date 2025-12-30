from django.db import models
from django.utils.translation import gettext_lazy as _

class Amenity(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="Lucide icon name")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Amenities"

class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_rate = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    amenities = models.ManyToManyField(Amenity, related_name="room_types")
    
    def __str__(self):
        return self.name

class Room(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', _('Available')
        OCCUPIED = 'occupied', _('Occupied')
        MAINTENANCE = 'maintenance', _('Maintenance')
        DIRTY = 'dirty', _('Dirty')

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="rooms")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    floor = models.IntegerField(default=1)

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type.name})"

class PricingRule(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="pricing_rules")
    start_date = models.DateField()
    end_date = models.DateField()
    rate_override = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.room_type.name} override: {self.start_date} to {self.end_date}"
