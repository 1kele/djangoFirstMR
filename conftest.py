from pathlib import Path

import pytest
from rest_framework.test import APIClient
from django.db import connection

from hotels.models import Hotels


@pytest.fixture(scope="session", autouse=True)
def create_test_schema(django_db_setup, django_db_blocker):
    schema_path = Path("db/schema.sql")
    sql = schema_path.read_text()

    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute(sql)

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def hotel():
    return Hotels.objects.create(
        name="Test Hotel", city="Moscow", founding_date="2000-01-01", stars=5
    )