from django.db import models
from django.utils.lorem_ipsum import paragraph
from rest_framework.exceptions import ValidationError


def validate_for_stars(value):
    if value > 5 or value < 1:
        raise ValidationError("Введите оценку от 1 до 5")


class Hotels(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    city = models.CharField(max_length=100, verbose_name="Город")
    address = models.TextField(verbose_name="Адресс", blank=True)
    founding_date = models.DateField(verbose_name="Дата основания")
    stars = models.IntegerField(validators=[validate_for_stars])

    def __str__(self):
        return f"{self.name}: {self.stars}"
