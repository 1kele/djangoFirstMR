from datetime import date

from django.core.exceptions import ValidationError
import pytest

from bookings.models import Bookings
from bookings.services import add_new_booking


@pytest.mark.parametrize(
    "start_date, end_date",
    [
        (date(2026, 10, 10), date(2026, 10, 15)),
        (date(2026, 10, 2), date(2026, 10, 11)),
        (date(2026, 10, 13), date(2026, 10, 20)),
        (date(2026, 10, 5), date(2026, 10, 17)),
        (date(2026, 10, 13), date(2026, 10, 14)),
    ],
)
@pytest.mark.django_db
def test_invalid_new_booking(room, booking, start_date, end_date):

    input_data = {
        "room": room,
        "start_date": start_date,
        "end_date": end_date,
    }

    with pytest.raises(ValidationError):
        add_new_booking(input_data)


@pytest.mark.parametrize(
    "start_date, end_date",
    [
        (date(2025, 9, 25), date(2025, 10, 3)),
        (date(2022, 1, 25), date(2025, 12, 31)),
        (date(2029, 12, 25), date(2029, 12, 26)),
    ],
)
@pytest.mark.django_db
def test_valid_new_booking(room, booking, start_date, end_date):

    input_data = {
        "room": room,
        "start_date": start_date,
        "end_date": end_date,
    }

    result = add_new_booking(input_data)
    days = (end_date - start_date).days

    assert result["price_per_night"] == room.price
    assert result["total_price"] == days * room.price
    assert result["status"] == Bookings.Status.CREATED
