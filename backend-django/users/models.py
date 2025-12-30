from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        SUPERADMIN = 'superadmin', _('Super Admin')
        MANAGER = 'manager', _('Manager')
        RECEPTIONIST = 'receptionist', _('Receptionist')
        HOUSEKEEPING = 'housekeeping', _('Housekeeping')
        GUEST = 'guest', _('Guest')

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.GUEST,
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_staff_member(self):
        return self.role in [self.Role.SUPERADMIN, self.Role.MANAGER, self.Role.RECEPTIONIST, self.Role.HOUSEKEEPING]
