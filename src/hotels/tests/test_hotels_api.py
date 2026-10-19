import pytest

from hotels.models import Hotels


@pytest.mark.django_db
def test_create_hotel(api_client):

    response = api_client.post(
        "/hotels/",
        {"name": "Test Hotel", "city": "Moscow", "founding_date": "2000-01-01", "stars": 5},
        format="json",
    )

    assert response.status_code == 201
    assert response.data["name"] == "Test Hotel"
    assert Hotels.objects.filter(name="Test Hotel").exists()


@pytest.mark.django_db
def test_get_hotel(api_client, hotel):

    response = api_client.get("/hotels/")

    assert response.status_code == 200
    assert response.data[0]["name"] == hotel.name
    assert len(response.data) == 1


@pytest.mark.django_db
def test_update_hotel(api_client, hotel):

    response = api_client.patch(
        f"/hotels/{hotel.id}/",
        {
            "name": "NEW NAME",
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.data["name"] == "NEW NAME"
    hotel.refresh_from_db()
    assert hotel.name == "NEW NAME"


@pytest.mark.django_db
def test_whole_update_hotel(api_client, hotel):
    response = api_client.put(
        f"/hotels/{hotel.id}/",
        {"name": "NEW ONE", "city": "IZHEVSK", "founding_date": "2001-11-11", "stars": 1},
        format="json",
    )

    assert response.status_code == 200
    hotel.refresh_from_db()
    assert hotel.city == "IZHEVSK"


@pytest.mark.django_db
def test_delete_hotel(api_client, hotel):

    response = api_client.delete(
        f"/hotels/{hotel.id}/",
    )

    assert response.status_code == 204
    assert not Hotels.objects.filter(pk=hotel.id).exists()
