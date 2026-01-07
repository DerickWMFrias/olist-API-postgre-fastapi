import pytest
import uuid
import logging

logger = logging.getLogger(__name__)

@pytest.mark.integration
def test_GET_users_1_successful_get_data(client):
    payload = {
        "email": "test@example.com",
        "password": "123456abc",
        "recovery_email": "rec.test@example.com"
    }
    data = client.post("/users/", json=payload).json()


    #logger.debug(data)
    #logger.debug(f"/users/{data["user_id"]}")
    response = client.get(f"/users?email={payload["email"]}&password={payload["password"]}")
    data = response.json()
    #logger.debug(data)
    assert response.status_code == 200

    assert "user_id" in data

    assert "email" in data
    assert data["email"] == payload["email"]


    response = client.get(f"/users?email={payload["email"]}&password={payload["password"]}&full_data=1")
    data = response.json()

    assert "user_id" in data

    assert "email" in data
    assert data["email"] == payload["email"]

    assert "hashed_password" not in data
    
    assert "recovery_email" in data
    assert data["recovery_email"] == payload["recovery_email"]



@pytest.mark.integration
def test_GET_users_1_not_found_user(client):
    dummy_email = "foobar@email.com"
    dummy_password = "abcd12#21dcbe"
    response = client.get(f"/users?email={dummy_email}&password={dummy_password}")

    assert response.status_code == 401


@pytest.mark.integration
def test_GET_users_1_invalid_user_id(client):
    response = client.get(f"/users?badarg=imbad")

    assert response.status_code == 422


@pytest.mark.integration
def test_POST_users_1_successful_register(client):
    payload = {
        "email": "test@example.com",
        "password": "123456abc",
        "recovery_email": "rec.test@example.com"
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert "user_id" in data
    assert "email" in data

    assert data["email"] == payload["email"]



@pytest.mark.integration
def test_POST_users_2_missing_payload_fields(client):
    payload = {
        "password": "123456abc",
        "recovery_email": "rec.test@example.com"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 422 or response.status_code == 500

    
    payload = {
        "email": "test@example.com",
        "recovery_email": "rec.test@example.com"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 422  or response.status_code == 500


    payload = {
        "email": "test@example.com",
        "password": "123456abc",
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 422  or response.status_code == 500


@pytest.mark.integration
def test_DELETE_users_1_delete_real_user(client):
    payload = {
        "email": "test@example.com",
        "password": "123456abc",
        "recovery_email": "rec.test@example.com"
    }

    data = client.post("/users/", json=payload).json()

    response = client.delete(f"/users/{data["user_id"]}")

    assert response.status_code == 204



@pytest.mark.integration
def test_DELETE_users_2_delete_fake_user(client):
    response = client.delete(f"/users/{str(uuid.uuid4())}")

    assert response.status_code == 404


@pytest.mark.integration
def test_DELETE_users_3_delete_invalid_uuid(client):
    response = client.delete("/users/123")

    assert response.status_code == 422





@pytest.mark.integration
def test_PATCH_users_1_patch_real_user(client):
    create_payload = {
        "email": "old@example.com",
        "password": "123456abc",
        "recovery_email": "rec@example.com"
    }
    user = client.post("/users/", json=create_payload).json()



    patch_payload_email = {
        "email": "new@example.com"
    }
    response = client.patch(
        f"/users/{user['user_id']}",
        json=patch_payload_email
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == patch_payload_email["email"]


@pytest.mark.integration
def test_PATCH_users_2_patch_fake_user(client):
    response = client.delete(f"/users/{str(uuid.uuid4())}")

    assert response.status_code == 404


@pytest.mark.integration
def test_PATCH_users_3_patch_invalid_uuid(client):
    response = client.patch("/users/123")

    assert response.status_code == 422