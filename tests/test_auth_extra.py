import uuid


def register_user(client, email, role="user", password="password123"):
    return client.post(
        "/auth/register",
        json={"email": email, "password": password, "role": role},
    )


def login_user(client, email, password="password123"):
    return client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )


def test_login_invalid_password(client):
    email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    res = register_user(client, email, role="user", password="password123")
    assert res.status_code == 201

    res = login_user(client, email, password="wrongpass")
    assert res.status_code == 401


def test_refresh_invalid_token(client):
    res = client.post("/auth/refresh", json={"refresh_token": "bad.token.value"})
    assert res.status_code == 401
