from pathlib import Path

import pytest
from rest_framework.test import APIClient
from django.db import connection

from bookings.models import Bookings
from hotels.models import Hotels, Rooms, Facilities


@pytest.fixture(scope="session", autouse=True)
def create_test_schema(django_db_setup, django_db_blocker):
    schema_path = Path("db/schema.sql")
    sql = schema_path.read_text()

    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute(sql)

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def hotel():
    return Hotels.objects.create(
        name="Test Hotel", city="Moscow", founding_date="2000-01-01", stars=5
    )


@pytest.fixture
def room(hotel, facility):
    room = Rooms.objects.create(hotel_id=hotel.id, price=10_000, occupancy=2)
    room.facilities.add(facility.id)
    return room


@pytest.fixture
def facility():
    Facilities.objects.create(name="Air Conditioner")
    return Facilities.objects.create(name="Wi-Fi")


@pytest.fixture
def booking(room):
    return Bookings.objects.create(
        room_id=room.id,
        start_date="2026-10-10",
        end_date="2026-10-15",
    )