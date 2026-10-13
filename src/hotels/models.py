from django.db import models
from django.utils.lorem_ipsum import paragraph
from rest_framework.exceptions import ValidationError


def validate_stars_range(value):
    if value > 5 or value < 1:
        raise ValidationError("Количество звёзд должно быть от 1 до 5")

def validate_positive_occupancy(value):
    if value <= 0:
        raise ValidationError("Вместимость должна быть больше 0")

def validate_positive_price(value):
    if value <= 0:
        raise ValidationError("Цена должна быть больше 0")


class Hotels(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    city = models.CharField(max_length=100, verbose_name="Город")
    address = models.TextField(verbose_name="Адресс", blank=True)
    founding_date = models.DateField(verbose_name="Дата основания")
    stars = models.IntegerField(validators=[validate_stars_range])

    def __str__(self):
        return f"Hotel #{self.pk} - {self.name}"

class Rooms(models.Model):
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive_price])
    occupancy = models.IntegerField(validators=[validate_positive_occupancy])
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"Room #{self.pk} - {self.hotel.name}"

