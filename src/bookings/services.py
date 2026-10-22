from django.db import transaction
from rest_framework.exceptions import ValidationError

from bookings.models import Bookings
from config.logging_setup import setup_logging
from hotels.models import Rooms

logger = setup_logging()


def add_new_booking(input_data: dict) -> Bookings:
    with transaction.atomic():
        room = input_data["room"]
        room = Rooms.objects.select_for_update().get(pk=room.id)
        start_date = input_data["start_date"]
        end_date = input_data["end_date"]

        booking_exists = Bookings.objects.filter(
            room_id=room.id,
            start_date__lt=end_date,
            end_date__gt=start_date,
            status__in=[Bookings.Status.CREATED, Bookings.Status.CONFIRMED],
        ).exists()

        if booking_exists:
            logger.warning(
                "Booking rejected: room_id={}, start_date={}, end_date={}",
                room.id,
                start_date,
                end_date,
            )
            raise ValidationError("Данный номер уже забронирован на выбранную вами дату")

        price = room.price
        total_price = price * (end_date - start_date).days

        booking = Bookings.objects.create(
            room=room,
            start_date=start_date,
            end_date=end_date,
            price_per_night=price,
            total_price=total_price,
            status=Bookings.Status.CREATED,
        )

        logger.info("Booking created: booking_id={}, room_id={}", booking.id, booking.room_id)

        return booking


def update_booking(old_data: Bookings, new_data: dict) -> Bookings:
    with transaction.atomic():
        if old_data.is_actual_sensitive_changes(new_data):
            pk = old_data.pk
            room = new_data.get("room", old_data.room)
            room = Rooms.objects.select_for_update().get(pk=room.id)
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
                logger.warning(
                    "Booking updating rejected: room_id={}, start_date={}, end_date={}",
                    room.id,
                    start_date,
                    end_date,
                )
                raise ValidationError("Данный номер уже забронирован на выбранную вами дату")

            total_price = price * (end_date - start_date).days

            old_data.price_per_night = price
            old_data.total_price = total_price

        for field, value in new_data.items():
            setattr(old_data, field, value)

        old_data.full_clean()
        old_data.save()
        logger.info("Booking updated: booking_id={}, room_id={}", old_data.pk, old_data.room.id)

        return old_data
