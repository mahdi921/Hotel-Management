from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from rooms.models import Room

class Booking(models.Model):
    class Status(models.TextChoices):
        RESERVED = 'reserved', _('Reserved')
        CHECKED_IN = 'checked_in', _('Checked In')
        CHECKED_OUT = 'checked_out', _('Checked Out')
        CANCELLED = 'cancelled', _('Cancelled')
        NO_SHOW = 'no_show', _('No Show')

    guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RESERVED)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Prevent overlapping bookings for the same room
        overlapping = Booking.objects.filter(
            room=self.room,
            check_in__lt=self.check_out,
            check_out__gt=self.check_in
        ).exclude(pk=self.pk).exclude(status__in=[self.Status.CANCELLED, self.Status.NO_SHOW])
        
        if overlapping.exists():
            raise ValidationError(_("This room is already booked for the selected dates."))

        if self.check_in >= self.check_out:
            raise ValidationError(_("Check-out date must be after check-in date."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.pk}: {self.guest.username} in {self.room.room_number}"
