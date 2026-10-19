import pytest

from hotels.models import Rooms


@pytest.mark.django_db
def test_create_room(api_client, hotel):

    response = api_client.post(
        f"/hotels/{hotel.id}/room/",
        {
            "price": 10_000,
            "occupancy": 2,
            "description": "Самая лучшая комната саратова",
            "created_at": "2026-10-16",
        },
        format="json",
    )

    assert response.status_code == 201
    assert "id" in response.data
    assert isinstance(response.data["id"], int)
    assert response.data["id"] > 0
    room_id = response.data["id"]
    assert Rooms.objects.filter(pk=room_id).exists()


@pytest.mark.django_db
def test_get_room(api_client, hotel, room):

    responses = api_client.get(
        f"/hotels/{hotel.id}/room/",
    )

    assert responses.status_code == 200
    assert responses.data[0]["id"] == room.id


@pytest.mark.django_db
def test_patch_room(api_client, hotel, room):

    responses = api_client.patch(
        f"/hotels/{hotel.id}/room/{room.id}/", {"price": 5_000}, format="json"
    )

    room.refresh_from_db()

    assert responses.status_code == 200
    assert room.price == 5_000
    assert responses.data["price"] == "5000.00"


@pytest.mark.django_db
def test_put_room(api_client, hotel, room):

    response = api_client.put(
        f"/hotels/{hotel.id}/room/{room.id}/",
        {
            "price": 250_000,
            "occupancy": 5,
            "description": "Уютный пятиместный номер с большой кроватью, рабочей зоной и собственной ванной комнатой",
            "created_at": "2024-09-06",
        },
        format="json",
    )

    room.refresh_from_db()

    assert response.status_code == 200
    assert response.data["price"] == "250000.00"
    assert room.price == 250_000


@pytest.mark.django_db
def test_put_delete(api_client, hotel, room):
    response = api_client.delete(f"/hotels/{hotel.id}/room/{room.id}/")

    assert response.status_code == 204
    assert not Rooms.objects.filter(pk=room.id).exists()
