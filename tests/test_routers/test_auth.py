def test_registration(client, mock_send_activation_email):
    response = client.post(
        "/register", json={"email": "test@example.com", "password": "testpass"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data["id"], int)
    assert data["email"] == "test@example.com"

    mock_send_activation_email.assert_awaited_once()
    args, kwargs = mock_send_activation_email.call_args
    assert args[0] == "test@example.com"


def test_register_with_existing_email(client, test_user, mock_send_activation_email):
    response = client.post(
        "/register", json={"email": "test@example.com", "password": "newpassword"}
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already" in data["detail"].lower()

    mock_send_activation_email.assert_not_awaited()


def test_activation(client, test_user, test_token):
    response = client.get(
        "/activate", params={"token": test_token}
    )
    assert response.status_code == 200
    data = response.json()
    assert "test@example.com" == data["email"]


def test_activation_nonexistent_user(client, test_token):
    response = client.get(
        "/activate", params={"token": test_token}
    )
    import logging; logging.error(response.json())
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]


def test_activation_bad_token(client):
    token = "bad.token"
    response = client.get(
        "/activate", params={"token": token}
    )
    assert response.status_code == 422


def test_login_user(client, test_user):
    response = client.post(
        "/login", data={"username": "test@example.com", "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_inactive_user(client, test_user_inactive):
    response = client.post(
        "/login", data={"username": "test1@example.com", "password": "testpass"}
    )
    assert response.status_code == 400
    data = response.json()
    assert "access_token" not in data
    assert "inactive" in data["detail"].lower()


def test_login_failed_user(client, test_user):
    response = client.post(
        "/login", data={"username": "test@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401
    data = response.json()
    assert "access_token" not in data


def test_login_invalid_email(client):
    response = client.post(
        "/login", data={"username": "testexample.com", "password": "wrongpass"}
    )
    assert response.status_code == 400
    data = response.json()
    assert "access_token" not in data
    assert "invalid email" in data["detail"].lower()
