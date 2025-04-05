def test_users_me_unauthenticated(client):
    response = client.get("/users/me")
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


def test_users_me_authenticated(client, test_user, test_token):
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["id"] == test_user.id
    assert "password" not in data


def test_users_list(client, test_token, test_user, test_user_inactive):
    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all('password' not in user for user in data)

    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {test_token}"},
        params={"limit": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {test_token}"},
        params={"skip": 2}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0
