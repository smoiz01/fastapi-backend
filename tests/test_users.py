def test_create_user(client):
    res = client.post(
        "/users/",
        json={"email": "user@example.com", "password": "secret123"},
    )

    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "user@example.com"
    assert "id" in data
    assert "created" in data
    assert "password" not in data

def test_existing_user_create(client, test_user):
    res = client.post(
        "/users/",
        json={"email": "user@example.com", "password": "secret123"},
    )

    assert res.status_code == 409
    assert "already exists" in res.json()["detail"]

def test_get_user(client, test_user):
    user_id = test_user["id"]
    email = test_user["email"]
    res = client.get(
        f'/users/{user_id}'
    )

    assert res.status_code == 200
    data = res.json()
    assert data["id"] == user_id
    assert data["email"] == email
    assert "created" in data

def test_get_user_not_found(client):
    res = client.get(
        f'/users/9999'
    )

    assert res.status_code == 404
    assert "not found" in res.json()["detail"]

