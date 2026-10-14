from django.db import models
from django.db.models import CharField

from .validators import validate_positive_occupancy, validate_positive_price, validate_stars_range


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
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[validate_positive_price]
    )
    occupancy = models.IntegerField(validators=[validate_positive_occupancy])
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now=True)
    facilities = models.ManyToManyField("Facilities", blank=True)

    def __str__(self):
        return f"Room #{self.pk} - {self.hotel.name}"


class Facilities(models.Model):
    name = CharField(max_length=255)

    def __str__(self):
        return f"Facility #{self.pk} - {self.name}"
