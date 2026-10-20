from django.core.exceptions import ValidationError

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


def update_booking(old_data: Bookings, new_data: dict) -> dict:
    pk = old_data.pk
    room = new_data.get("room", old_data.room)
    start_date = new_data.get("start_date", old_data.start_date)
    end_date = new_data.get("end_date", old_data.end_date)
    price = new_data.get("price_per_night", room.price)

    booking_exists = (
        Bookings.objects.filter(
            room_id=room.id,
            start_date__lt=end_date,
            end_date__gt=start_date,
            status__in=[Bookings.Status.CREATED, Bookings.Status.CONFIRMED],
        )
        .exclude(pk=pk)
        .exists()
    )

    if booking_exists:
        raise ValidationError("Данный номер уже забронирован на выбранную вами дату")

    total_price = price * (end_date - start_date).days

    booking_data = {
        "price_per_night": price,
        "total_price": total_price,
        "status": Bookings.Status.CREATED,
    }

    return booking_data
