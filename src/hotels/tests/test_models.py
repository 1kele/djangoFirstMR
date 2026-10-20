from django.db import IntegrityError
import pytest

from bookings.models import Bookings
from hotels.models import Facilities, Hotels, Rooms


@pytest.mark.django_db
def test_delete_hotels_cascade():
    hotel = Hotels.objects.create(
        name="Test Hotel", city="Moscow", founding_date="2000-01-01", stars=5
    )

    Rooms.objects.create(
        hotel=hotel,
        price=10000,
        occupancy=2,
    )

    hotel.delete()

    assert Rooms.objects.count() == 0


@pytest.mark.django_db
def test_add_facility_to_room():
    hotel = Hotels.objects.create(
        name="Test Hotel", city="Moscow", founding_date="2000-01-01", stars=5
    )

    room = Rooms.objects.create(hotel=hotel, price=10000, occupancy=2)

    facility = Facilities.objects.create(name="Test")

    room.facilities.add(facility)

    assert facility in room.facilities.all()


@pytest.mark.django_db
def test_check_unique():
    Hotels.objects.create(name="Test Hotel", city="Moscow", founding_date="2000-01-01", stars=5)

    with pytest.raises(IntegrityError):
        Hotels.objects.create(name="Test Hotel", city="sdfsf", founding_date="2010-01-01", stars=5)


@pytest.mark.django_db
def test_delete_room_cascade(room, booking):
    room.delete()
    assert Bookings.objects.count() == 0
