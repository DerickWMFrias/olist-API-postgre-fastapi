import pytest
import uuid
import logging

logger = logging.getLogger(__name__)




@pytest.mark.integration
def test_GET_geo_coordinates_1_successful_get_data(client):
    payload = {
        "geolocation_zip_code_prefix": "31322599",
        "lat": -23.415779617114935,
        "lng": -46.41607223296136
    }

    response = client.post("/geo/coordinates", json=payload)

    response = client.get(f"/geo/coordinates?zipcode_prefix={payload["geolocation_zip_code_prefix"]}")
    data = response.json()

    assert response.status_code == 200

    assert "geolocation_zip_code_prefix" in data
    assert "lat" in data
    assert "lng" in data


@pytest.mark.integration
def test_GET_geo_coordinates_2_not_found_user(client):
    dummy_email = "49205039"
    response = client.get(f"/geo/coordinates?zipcode_prefix={dummy_email}")

    assert response.status_code == 404


@pytest.mark.integration
def test_GET_geo_coordinates_3_too_long_zipcode(client):
    response = client.get(f"/geo/coordinates?zipcode_prefix=12345678910")

    assert response.status_code == 422


@pytest.mark.integration
def test_POST_geo_coordinates_1_successful_register(client):
    payload = {
        "geolocation_zip_code_prefix": "31322599",
        "lat": -23.415779617114935,
        "lng": -46.41607223296136
    }

    response = client.post("/geo/coordinates", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert "geolocation_zip_code_prefix" in data
    assert "lat" in data
    assert "lng" in data


    assert data["geolocation_zip_code_prefix"] == payload["geolocation_zip_code_prefix"]
    assert data["lat"] == str(payload["lat"])
    assert data["lng"] == str(payload["lng"])



@pytest.mark.integration
def test_POST_geo_coordinates_2_missing_payload_fields(client):
    payload = {
        "geolocation_zip_code_prefix": "31322599",
        "lat": -23.415779617114935,
    }

    response = client.post("/geo/coordinates", json=payload)
    assert response.status_code == 422

