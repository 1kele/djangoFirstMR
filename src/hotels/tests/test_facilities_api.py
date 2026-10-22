import pytest

from hotels.models import Facilities


@pytest.mark.django_db
def test_create_facility(api_client):

    response = api_client.post("/hotels/facilities/", {"name": "Panoramic Windows"}, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Panoramic Windows"
    assert Facilities.objects.filter(name="Panoramic Windows").count() == 1


@pytest.mark.django_db
def test_get_facilities(api_client, facility):

    response = api_client.get("/hotels/facilities/")

    names = [item["name"] for item in response.data]
    assert response.status_code == 200
    assert "Air Conditioner" in names
    assert "Wi-Fi" in names


@pytest.mark.django_db
def test_get_facility(api_client, facility):
    response = api_client.get(f"/hotels/facilities/{facility.id}/")

    assert response.status_code == 200
    assert response.data["name"] == facility.name


@pytest.mark.django_db
def test_get_put(api_client, facility):

    response = api_client.put(
        f"/hotels/facilities/{facility.id}/", {"name": "King Size Bed"}, format="json"
    )

    facility.refresh_from_db()

    assert response.status_code == 200
    assert response.data["name"] == "King Size Bed"
    assert response.data["name"] == facility.name


@pytest.mark.django_db
def test_get_delete(api_client, facility):

    response = api_client.delete(f"/hotels/facilities/{facility.id}/")

    assert response.status_code == 204
    assert not Facilities.objects.filter(pk=facility.id).exists()
