import pytest
from rest_framework.exceptions import ValidationError

from hotels.validators import (
    validate_positive_occupancy,
    validate_positive_price,
    validate_stars_range,
)


@pytest.mark.parametrize("value", [0, -1, 6, 100000])
def test_invalid_stars(value):
    with pytest.raises(ValidationError):
        validate_stars_range(value)


@pytest.mark.parametrize("value", [1, 3, 5])
def test_valid_stars(value):
    validate_stars_range(value)


@pytest.mark.parametrize("value", [-1, -1000])
def test_invalid_occupancy(value):
    with pytest.raises(ValidationError):
        validate_positive_occupancy(value)


@pytest.mark.parametrize("value", [1, 10])
def test_valid_occupancy(value):
    validate_positive_occupancy(value)


@pytest.mark.parametrize("value", [-1, -1000, 0])
def test_invalid_price(value):
    with pytest.raises(ValidationError):
        validate_positive_price(value)


@pytest.mark.parametrize("value", [1, 1000, 9999])
def test_valid_price(value):
    validate_positive_price(value)
