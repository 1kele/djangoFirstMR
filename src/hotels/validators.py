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
