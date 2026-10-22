from django.core.exceptions import ValidationError
import pytest

from bookings.models import Bookings


@pytest.mark.django_db
def test_invalid_dates(room):

    booking = Bookings(
        room_id=room.id,
        start_date="2026-10-10",
        end_date="2026-10-05",
        price_per_night=10_000,
        total_price=50_000,
    )

    with pytest.raises(ValidationError):
        booking.full_clean()


@pytest.mark.django_db
def test_valid_dates(room):

    booking = Bookings(
        room_id=room.id,
        start_date="2026-10-10",
        end_date="2026-10-15",
        price_per_night=10_000,
        total_price=50_000,
    )

    booking.full_clean()
