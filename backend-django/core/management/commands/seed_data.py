from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rooms.models import RoomType, Room, Amenity
from bookings.models import Booking
from billing.models import Invoice, LineItem
from datetime import date, timedelta
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # 1. Create Admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@hotel.local', 'adminpass', role='superadmin')
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # 2. Create Guests
        guests = []
        for i in range(5):
            username = f'guest{i+1}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username, f'{username}@example.com', 'password', role='guest')
                guests.append(user)
            else:
                guests.append(User.objects.get(username=username))
        self.stdout.write(self.style.SUCCESS(f'Created {len(guests)} guests'))

        # 3. Amenities
        amenities = ['Wi-Fi', 'TV', 'AC', 'Projector', 'Mini Bar', 'Ocean View']
        created_amenities = []
        for name in amenities:
            obj, _ = Amenity.objects.get_or_create(name=name)
            created_amenities.append(obj)

        # 4. Room Types
        types = [
            ('Standard User', 100.00, 2),
            ('Deluxe Suite', 250.00, 4),
            ('Penthouse', 500.00, 6)
        ]
        room_types = []
        for name, rate, cap in types:
            rt, created = RoomType.objects.get_or_create(
                name=name,
                defaults={'description': f'A lovely {name}', 'base_rate': rate, 'capacity': cap}
            )
            if created:
                rt.amenities.set(random.sample(created_amenities, 3))
            room_types.append(rt)

        # 5. Rooms
        created_rooms = []
        for i in range(1, 11):
            room_number = f'{100+i}'
            rt = random.choice(room_types)
            room, created = Room.objects.get_or_create(
                room_number=room_number,
                defaults={'room_type': rt, 'floor': 1}
            )
            created_rooms.append(room)
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_rooms)} rooms'))

        # 6. Bookings
        today = date.today()
        for i in range(10):
            guest = random.choice(guests)
            room = random.choice(created_rooms)
            start_date = today + timedelta(days=random.randint(1, 30))
            end_date = start_date + timedelta(days=random.randint(1, 5))
            
            # Simple overlap check for seed data
            if not Booking.objects.filter(room=room, check_in__lt=end_date, check_out__gt=start_date).exists():
                b = Booking.objects.create(
                    guest=guest,
                    room=room,
                    check_in=start_date,
                    check_out=end_date,
                    total_price=room.room_type.base_rate * (end_date - start_date).days,
                    status='reserved'
                )
                
                # Invoice
                inv = Invoice.objects.create(
                    booking=b,
                    invoice_number=f"INV-{b.id}",
                    due_date=end_date,
                )
                LineItem.objects.create(
                    invoice=inv,
                    description=f"Room Charge ({room.room_type.name})",
                    quantity=(end_date - start_date).days,
                    unit_price=room.room_type.base_rate
                )

        self.stdout.write(self.style.SUCCESS('Seeding completed!'))
