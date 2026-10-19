from pathlib import Path

import pytest
from django.db import connection


@pytest.fixture(scope="session", autouse=True)
def create_test_schema(django_db_setup, django_db_blocker):
    schema_path = Path("db/schema.sql")
    sql = schema_path.read_text()

    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute(sql)