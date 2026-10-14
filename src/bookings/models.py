from django.core.exceptions import ValidationError
from django.db import models

from hotels.models import Rooms
from hotels.validators import validate_positive_price


class Bookings(models.Model):
    class Status(models.TextChoices):
        CREATED = "created", "Создан"
        CONFIRMED = "confirmed", "Подтвержден"
        CANCELLED = "cancelled", "Отменен"
        COMPLETED = "completed", "Завершен"

    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price_per_night = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[validate_positive_price]
    )
    total_price = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[validate_positive_price]
    )
    status = models.CharField(choices=Status.choices, default=Status.CREATED)

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError("Дата выезда должа быть позже даты заезда")
