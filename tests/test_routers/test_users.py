import pytest


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


def test_users_unauthenticated(client):
    response = client.get("/users/")
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


@pytest.mark.parametrize("skip,limit,n_users", [
    (0, 100, 2),
    (2, 100, 0),
    (1, 100, 1),
    (0, 1, 1),
])
def test_users_list(
        skip, limit, n_users,
        client, test_token, test_user, test_user_inactive,
):
    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {test_token}"},
        params={"skip": skip, "limit": limit},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == n_users
    assert all("password" not in user for user in data) is True
