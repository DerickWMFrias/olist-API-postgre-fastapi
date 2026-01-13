import pytest
import uuid
import logging

logger = logging.getLogger(__name__)




@pytest.mark.integration
def test_GET_geo_coordinate_1_successful_get_data(client):
    payload = {
        "geolocation_zip_code_prefix": "31322599",
        "lat": -23.415779617114935,
        "lng": -46.41607223296136
    }

    response = client.post("/geo/coordinate", json=payload)
    data = response.json()

    response = client.get(f"/geo/coordinate?coordinate_id={data["coordinate_id"]}")
    data = response.json()

    assert response.status_code == 200

    assert "geolocation_zip_code_prefix" in data
    assert "lat" in data
    assert "lng" in data


@pytest.mark.integration
def test_GET_geo_coordinate_2_not_found_user(client):
    dummy_id = uuid.uuid4()
    response = client.get(f"/geo/coordinate?coordinate_id={dummy_id}")

    assert response.status_code == 404


@pytest.mark.integration
def test_GET_geo_coordinate_3_bad_uuid(client):
    response = client.get(f"/geo/coordinate?coordinate_id=12345678910")

    assert response.status_code == 422


@pytest.mark.integration
def test_POST_geo_coordinate_1_successful_register(client):
    payload = {
        "geolocation_zip_code_prefix": "31322599",
        "lat": -23.415779617114935,
        "lng": -46.41607223296136
    }

    response = client.post("/geo/coordinate", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert "geolocation_zip_code_prefix" in data
    assert "lat" in data
    assert "lng" in data


    assert data["geolocation_zip_code_prefix"] == payload["geolocation_zip_code_prefix"]
    assert data["lat"] == str(payload["lat"])
    assert data["lng"] == str(payload["lng"])



@pytest.mark.integration
def test_POST_geo_coordinate_2_missing_payload_fields(client):
    payload = {
        "geolocation_zip_code_prefix": "31322599",
        "lat": -23.415779617114935,
    }

    response = client.post("/geo/coordinate", json=payload)
    assert response.status_code == 422






@pytest.mark.integration
def test_GET_geo_coordinates_1_successful_get_data(client):
    df = 0.15
    created_ids = []

    for i in range(40):
        payload = {
            "geolocation_zip_code_prefix": "31322599",
            "lat": -23.415779617114935 + i*df,
            "lng": -46.41607223296136 + i*df
        }
        response = client.post("/geo/coordinate", json=payload)
        created_ids.append(response.json()["coordinate_id"])
        assert response.status_code == 201

    response = client.get(f"/geo/coordinates/31322599?limit=20")
    data = response.json()

    assert response.status_code == 200

    assert "items" in data
    assert "next_cursor" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) == 20

    for item in data["items"]:
        assert isinstance(item, dict)

        assert "geolocation_zip_code_prefix" in item
        assert "lat" in item
        assert "lng" in item
        assert "coordinate_id" in item

        assert item["coordinate_id"] in created_ids

    response = client.get(f"/geo/coordinates/31322599?limit=20&cursor={data["next_cursor"]}")
    data = response.json()

    assert response.status_code == 200    

    for item in data["items"]:
        assert isinstance(item, dict)

        assert item["coordinate_id"] in created_ids

    assert data["next_cursor"] is None



@pytest.mark.integration
def test_DELETE_geo_coordinates_1_successful_delete(client):
    payload = {
        "geolocation_zip_code_prefix": "31322599",
        "lat": -23.415779617114935,
        "lng": -46.41607223296136
    }

    response = client.post("/geo/coordinate", json=payload)
    data = response.json()
    assert response.status_code == 201


    response = client.delete(f"/geo/coordinate/{data["coordinate_id"]}")
    assert response.status_code == 204