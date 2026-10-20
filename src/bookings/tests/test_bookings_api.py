import pytest

from bookings.models import Bookings


@pytest.mark.django_db
def test_create_booking(api_client, room):

    response = api_client.post(
        "/bookings/",
        {
            "room": room.id,
            "start_date": "2026-10-12",
            "end_date": "2026-10-15",
        },
        format="json",
    )

    assert response.status_code == 201
    assert "id" in response.data
    booking_id = response.data["id"]
    assert Bookings.objects.filter(pk=booking_id).exists()


@pytest.mark.django_db
def test_get_bookings(api_client, booking, room):

    api_client.post(
        "/bookings/",
        {
            "room": room.id,
            "start_date": "2026-10-20",
            "end_date": "2026-10-25",
        },
        format="json",
    )

    response = api_client.get("/bookings/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["id"] == booking.id


@pytest.mark.django_db
def test_get_booking(api_client, booking):

    response = api_client.get(f"/bookings/{booking.id}/")

    assert response.status_code == 200
    assert response.data["id"] == booking.id


@pytest.mark.django_db
def test_put_booking(api_client, booking, room):

    response = api_client.put(
        f"/bookings/{booking.id}/",
        {
            "room": room.id,
            "start_date": "2026-10-11",
            "end_date": "2026-10-19",
            "price_per_night": room.price,
            "total_price": room.price * 5,
            "status": Bookings.Status.CONFIRMED,
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.data["id"] == booking.id


@pytest.mark.django_db
def test_patch_booking(api_client, booking, room):

    response = api_client.patch(
        f"/bookings/{booking.id}/",
        {
            "end_date": "2026-10-17",
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.data["id"] == booking.id


@pytest.mark.django_db
def test_delete_booking(api_client, booking, room):

    response = api_client.delete(f"/bookings/{booking.id}/")

    assert response.status_code == 204
    assert not Bookings.objects.filter(pk=booking.id).exists()


@pytest.mark.django_db
def test_get_bookings_from_room(api_client, booking, room):

    response = api_client.get(f"/bookings/room/{room.id}/")

    assert response.status_code == 200
    assert response.data[0]["id"] == booking.id
    assert response.data[0]["room"] == room.id
