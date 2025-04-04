def test_registration(client):
    response = client.post(
        "/register", json={"email": "test@example.com", "password": "testpass"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data['id'], int)
    assert data["email"] == "test@example.com"


def test_register_with_existing_email(client, test_user):
    response = client.post(
        "/register",
        json={"email": "test@example.com", "password": "newpassword"}
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already" in data["detail"].lower()


def test_login_user(client, test_user):
    response = client.post(
        "/login",
        data={"username": "test@example.com", "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_failed_user(client, test_user):
    response = client.post(
        "/login",
        data={"username": "test@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401
    data = response.json()
    assert "access_token" not in data
