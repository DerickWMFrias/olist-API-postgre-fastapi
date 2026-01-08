import pytest
import uuid
import logging

logger = logging.getLogger(__name__)



@pytest.mark.integration
def test_GET_geo_1_successful_get_data(client):
    payload = {
        "geolocation_zip_code_prefix": "31322599",
        "geolocation_city": "São Thomé das Letras",
        "geolocation_state": "SP"
    }

    response = client.post("/geo/", json=payload)

    response = client.get(f"/geo?zipcode_prefix={payload["geolocation_zip_code_prefix"]}")
    data = response.json()

    assert response.status_code == 200

    assert "geolocation_zip_code_prefix" in data
    assert "geolocation_city" in data
    assert "geolocation_state" in data


@pytest.mark.integration
def test_GET_geo_2_not_found_user(client):
    dummy_email = "49205039"
    response = client.get(f"/geo?zipcode_prefix={dummy_email}")

    assert response.status_code == 404


@pytest.mark.integration
def test_GET_geo_3_too_long_zipcode(client):
    response = client.get(f"/geo?zipcode_prefix=12345678910")

    assert response.status_code == 422


@pytest.mark.integration
def test_POST_geo_1_successful_register(client):
    payload = {
        "geolocation_zip_code_prefix": "31322599",
        "geolocation_city": "São Thomé das Letras",
        "geolocation_state": "SP"
    }

    response = client.post("/geo/", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert "geolocation_zip_code_prefix" in data
    assert "geolocation_city" in data
    assert "geolocation_state" in data


    assert data["geolocation_zip_code_prefix"] == payload["geolocation_zip_code_prefix"]
    assert data["geolocation_city"] == payload["geolocation_city"]
    assert data["geolocation_state"] == payload["geolocation_state"]



@pytest.mark.integration
def test_POST_geo_2_missing_payload_fields(client):
    payload = {
        "geolocation_zip_code_prefix": "31322599",
        "geolocation_city": "São Thomé das Letras"
    }

    response = client.post("/geo/", json=payload)
    assert response.status_code == 422

