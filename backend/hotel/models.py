"""
Hotel Management System - Models
Persian/Farsi Edition

This module contains all domain models for the hotel management system:
- User (Custom user model for staff)
- RoomType (Categories of rooms)
- Room (Individual rooms with status tracking)
- Guest (Hotel guests)
- Booking (Reservations with date tracking)
- Payment (Financial transactions)
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


class User(AbstractUser):
    """
    Custom User model for hotel staff.
    کاربران سیستم (کارمندان هتل)
    """
    
    class Role(models.TextChoices):
        ADMIN = 'admin', _('مدیر')
        MANAGER = 'manager', _('سرپرست')
        RECEPTIONIST = 'receptionist', _('پذیرش')
        HOUSEKEEPING = 'housekeeping', _('خدمات')
    
    role = models.CharField(
        _('نقش'),
        max_length=20,
        choices=Role.choices,
        default=Role.RECEPTIONIST,
    )
    phone = models.CharField(_('شماره تلفن'), max_length=15, blank=True)
    
    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')
    
    def __str__(self):
        return f"{self.get_full_name() or self.username}"


class RoomType(models.Model):
    """
    Room categories/types.
    انواع اتاق
    """
    
    class BedType(models.TextChoices):
        SINGLE = 'single', _('تک نفره')
        DOUBLE = 'double', _('دو نفره')
        TWIN = 'twin', _('دو تخت مجزا')
        QUEEN = 'queen', _('کویین')
        KING = 'king', _('کینگ')
        SUITE = 'suite', _('سوئیت')
    
    name = models.CharField(_('نام نوع اتاق'), max_length=100)
    description = models.TextField(_('توضیحات'), blank=True)
    bed_type = models.CharField(
        _('نوع تخت'),
        max_length=20,
        choices=BedType.choices,
        default=BedType.DOUBLE,
    )
    capacity = models.PositiveSmallIntegerField(
        _('ظرفیت'),
        default=2,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    base_price = models.DecimalField(
        _('قیمت پایه (شبانه)'),
        max_digits=12,
        decimal_places=0,
        default=Decimal('1000000'),
        help_text=_('قیمت به ریال'),
    )
    amenities = models.TextField(
        _('امکانات'),
        blank=True,
        help_text=_('امکانات اتاق (هر خط یک مورد)'),
    )
    
    class Meta:
        verbose_name = _('نوع اتاق')
        verbose_name_plural = _('انواع اتاق')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Room(models.Model):
    """
    Individual hotel room.
    اتاق‌های هتل
    """
    
    class Status(models.TextChoices):
        CLEAN = 'clean', _('تمیز')
        DIRTY = 'dirty', _('نیاز به نظافت')
        OCCUPIED = 'occupied', _('اشغال')
        MAINTENANCE = 'maintenance', _('در حال تعمیر')
    
    class View(models.TextChoices):
        SEA = 'sea', _('دریا')
        CITY = 'city', _('شهر')
        GARDEN = 'garden', _('باغ')
        MOUNTAIN = 'mountain', _('کوه')
        POOL = 'pool', _('استخر')
        NONE = 'none', _('بدون منظره')
    
    room_number = models.CharField(_('شماره اتاق'), max_length=10, unique=True)
    floor = models.PositiveSmallIntegerField(_('طبقه'), default=1)
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.PROTECT,
        related_name='rooms',
        verbose_name=_('نوع اتاق'),
    )
    status = models.CharField(
        _('وضعیت'),
        max_length=20,
        choices=Status.choices,
        default=Status.CLEAN,
    )
    view = models.CharField(
        _('منظره'),
        max_length=20,
        choices=View.choices,
        default=View.CITY,
    )
    is_active = models.BooleanField(_('فعال'), default=True)
    notes = models.TextField(_('یادداشت'), blank=True)
    
    class Meta:
        verbose_name = _('اتاق')
        verbose_name_plural = _('اتاق‌ها')
        ordering = ['floor', 'room_number']
    
    def __str__(self):
        return f"اتاق {self.room_number} - {self.room_type.name}"
    
    @property
    def nightly_rate(self):
        """Get the current nightly rate for this room."""
        return self.room_type.base_price


class Guest(models.Model):
    """
    Hotel guest information.
    اطلاعات مهمانان
    """
    
    class Gender(models.TextChoices):
        MALE = 'male', _('مرد')
        FEMALE = 'female', _('زن')
        OTHER = 'other', _('سایر')
    
    first_name = models.CharField(_('نام'), max_length=100)
    last_name = models.CharField(_('نام خانوادگی'), max_length=100)
    national_id = models.CharField(
        _('کد ملی'),
        max_length=20,
        unique=True,
        blank=True,
        null=True,
    )
    passport_number = models.CharField(
        _('شماره پاسپورت'),
        max_length=50,
        blank=True,
    )
    gender = models.CharField(
        _('جنسیت'),
        max_length=10,
        choices=Gender.choices,
        default=Gender.MALE,
    )
    phone = models.CharField(_('شماره تلفن'), max_length=15)
    email = models.EmailField(_('ایمیل'), blank=True)
    address = models.TextField(_('آدرس'), blank=True)
    date_of_birth = models.DateField(_('تاریخ تولد'), null=True, blank=True)
    nationality = models.CharField(_('ملیت'), max_length=50, default='ایرانی')
    created_at = models.DateTimeField(_('تاریخ ثبت'), auto_now_add=True)
    notes = models.TextField(_('یادداشت'), blank=True)
    
    class Meta:
        verbose_name = _('مهمان')
        verbose_name_plural = _('مهمانان')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Booking(models.Model):
    """
    Room reservation/booking.
    رزرو اتاق
    """
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('در انتظار')
        CONFIRMED = 'confirmed', _('تایید شده')
        CHECKED_IN = 'checked_in', _('ورود انجام شد')
        CHECKED_OUT = 'checked_out', _('خروج انجام شد')
        CANCELLED = 'cancelled', _('لغو شده')
        NO_SHOW = 'no_show', _('عدم مراجعه')
    
    # Booking identification
    booking_number = models.CharField(
        _('شماره رزرو'),
        max_length=20,
        unique=True,
        editable=False,
    )
    
    # Relations
    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name='bookings',
        verbose_name=_('اتاق'),
    )
    guest = models.ForeignKey(
        Guest,
        on_delete=models.PROTECT,
        related_name='bookings',
        verbose_name=_('مهمان'),
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='bookings_created',
        verbose_name=_('ثبت کننده'),
    )
    
    # Dates
    check_in_date = models.DateField(_('تاریخ ورود'))
    check_out_date = models.DateField(_('تاریخ خروج'))
    actual_check_in = models.DateTimeField(_('زمان ورود واقعی'), null=True, blank=True)
    actual_check_out = models.DateTimeField(_('زمان خروج واقعی'), null=True, blank=True)
    
    # Check-in/out times (default: 14:00 check-in, 12:00 check-out)
    CHECK_IN_TIME = "14:00"
    CHECK_OUT_TIME = "12:00"
    
    # Status
    status = models.CharField(
        _('وضعیت'),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    
    # Guests count
    adults = models.PositiveSmallIntegerField(_('بزرگسالان'), default=1)
    children = models.PositiveSmallIntegerField(_('کودکان'), default=0)
    
    # Financial
    nightly_rate = models.DecimalField(
        _('نرخ شبانه'),
        max_digits=12,
        decimal_places=0,
    )
    service_charge = models.DecimalField(
        _('هزینه خدمات'),
        max_digits=12,
        decimal_places=0,
        default=Decimal('0'),
    )
    discount = models.DecimalField(
        _('تخفیف'),
        max_digits=12,
        decimal_places=0,
        default=Decimal('0'),
    )
    
    # Metadata
    notes = models.TextField(_('یادداشت'), blank=True)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاریخ بروزرسانی'), auto_now=True)
    
    class Meta:
        verbose_name = _('رزرو')
        verbose_name_plural = _('رزروها')
        ordering = ['-check_in_date']
    
    def __str__(self):
        return f"{self.booking_number} - {self.guest.full_name}"
    
    def save(self, *args, **kwargs):
        # Generate booking number if not exists
        if not self.booking_number:
            self.booking_number = self._generate_booking_number()
        
        # Set nightly rate from room if not set
        if not self.nightly_rate:
            self.nightly_rate = self.room.nightly_rate
        
        super().save(*args, **kwargs)
    
    def _generate_booking_number(self):
        """Generate unique booking number: HB-YYYYMMDD-XXXX"""
        today = timezone.now().strftime('%Y%m%d')
        last_booking = Booking.objects.filter(
            booking_number__startswith=f'HB-{today}-'
        ).order_by('-booking_number').first()
        
        if last_booking:
            last_num = int(last_booking.booking_number.split('-')[-1])
            new_num = last_num + 1
        else:
            new_num = 1
        
        return f"HB-{today}-{new_num:04d}"
    
    @property
    def nights(self):
        """Calculate number of nights."""
        return (self.check_out_date - self.check_in_date).days
    
    @property
    def total_amount(self):
        """Calculate total bill: (nights * rate) + service - discount"""
        base = self.nightly_rate * self.nights
        return base + self.service_charge - self.discount
    
    @property
    def is_today_checkin(self):
        """Check if this booking has check-in today."""
        return self.check_in_date == timezone.now().date()
    
    @property
    def is_today_checkout(self):
        """Check if this booking has check-out today."""
        return self.check_out_date == timezone.now().date()


class Payment(models.Model):
    """
    Payment/transaction records.
    پرداخت‌ها
    """
    
    class Method(models.TextChoices):
        CASH = 'cash', _('نقدی')
        CARD = 'card', _('کارت')
        TRANSFER = 'transfer', _('انتقال بانکی')
        ONLINE = 'online', _('آنلاین')
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('در انتظار')
        COMPLETED = 'completed', _('تکمیل شده')
        FAILED = 'failed', _('ناموفق')
        REFUNDED = 'refunded', _('مسترد شده')
    
    booking = models.ForeignKey(
        Booking,
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name=_('رزرو'),
    )
    amount = models.DecimalField(
        _('مبلغ'),
        max_digits=12,
        decimal_places=0,
    )
    method = models.CharField(
        _('روش پرداخت'),
        max_length=20,
        choices=Method.choices,
        default=Method.CASH,
    )
    status = models.CharField(
        _('وضعیت'),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    reference_number = models.CharField(
        _('شماره پیگیری'),
        max_length=100,
        blank=True,
    )
    received_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='payments_received',
        verbose_name=_('دریافت کننده'),
    )
    notes = models.TextField(_('یادداشت'), blank=True)
    created_at = models.DateTimeField(_('تاریخ پرداخت'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('پرداخت')
        verbose_name_plural = _('پرداخت‌ها')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.booking.booking_number} - {self.amount:,.0f} ریال"
