import uuid


def register_user(client, email, role="user", password="password123"):
    res = client.post(
        "/auth/register",
        json={"email": email, "password": password, "role": role},
    )
    return res


def login_user(client, email, password="password123"):
    return client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_users_crud_flow(client):
    email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    res = register_user(client, email, role="user")
    assert res.status_code == 201
    user = res.json()
    user_id = user["id"]

    res = login_user(client, email)
    assert res.status_code == 200
    token = res.json()["access_token"]

    res = client.get("/users/", headers=auth_headers(token))
    assert res.status_code == 200
    assert any(u["id"] == user_id for u in res.json())

    res = client.get(f"/users/{user_id}", headers=auth_headers(token))
    assert res.status_code == 200
    assert res.json()["email"] == email

    new_email = f"updated_{uuid.uuid4().hex[:8]}@example.com"
    res = client.patch(
        f"/users/{user_id}",
        headers=auth_headers(token),
        json={"email": new_email},
    )
    assert res.status_code == 200
    assert res.json()["email"] == new_email

    res = client.delete(f"/users/{user_id}", headers=auth_headers(token))
    assert res.status_code == 204

    res = client.get(f"/users/{user_id}", headers=auth_headers(token))
    assert res.status_code in (401, 404)


def test_users_duplicate_email(client):
    email = f"dup_{uuid.uuid4().hex[:8]}@example.com"
    res = register_user(client, email, role="user")
    assert res.status_code == 201

    res = register_user(client, email, role="user")
    assert res.status_code == 400


def test_users_requires_auth(client):
    res = client.get("/users/")
    assert res.status_code in (401, 403)

    res = client.get(f"/users/{uuid.uuid4()}")
    assert res.status_code in (401, 403)
