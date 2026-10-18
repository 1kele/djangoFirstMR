from rest_framework.exceptions import ValidationError

from bookings.models import Bookings


def add_new_booking(input_data: dict) -> dict:

    room = input_data["room"]
    start_date = input_data["start_date"]
    end_date = input_data["end_date"]

    booking_exists = Bookings.objects.filter(
        room_id=room.id,
        start_date__lt=end_date,
        end_date__gt=start_date,
        status__in=[Bookings.Status.CREATED, Bookings.Status.CONFIRMED],
    ).exists()

    if booking_exists:
        raise ValidationError("Данный номер уже забронирован на выбранную вами дату")

    price = room.price
    total_price = price * (end_date - start_date).days

    booking_data = {
        "price_per_night": price,
        "total_price": total_price,
        "status": Bookings.Status.CREATED,
    }

    return booking_data
