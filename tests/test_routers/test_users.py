def test_users_me_unauthenticated(client):
    response = client.get("/users/me")
    assert response.status_code == 401


def test_users_me_authenticated(client, test_user, test_token):
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["id"] == test_user.id