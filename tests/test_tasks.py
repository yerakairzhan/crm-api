import uuid


def register_and_login(client, email, role):
    res = client.post(
        "/auth/register",
        json={"email": email, "password": "password123", "role": role},
    )
    assert res.status_code == 201
    res = client.post(
        "/auth/login",
        json={"email": email, "password": "password123"},
    )
    assert res.status_code == 200
    return res.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_task_create_requires_user_role(client):
    author_email = f"author_{uuid.uuid4().hex[:8]}@example.com"
    author_token = register_and_login(client, author_email, "author")

    res = client.post(
        "/tasks/",
        headers=auth_headers(author_token),
        json={"description": "Task", "comment": "Nope"},
    )
    assert res.status_code == 403


def test_task_owner_only_update_delete(client):
    user1 = f"user_{uuid.uuid4().hex[:8]}@example.com"
    user2 = f"user_{uuid.uuid4().hex[:8]}@example.com"

    token1 = register_and_login(client, user1, "user")
    token2 = register_and_login(client, user2, "user")

    res = client.post(
        "/tasks/",
        headers=auth_headers(token1),
        json={"description": "Task", "comment": "Init"},
    )
    assert res.status_code == 201
    task_id = res.json()["id"]

    res = client.patch(
        f"/tasks/{task_id}",
        headers=auth_headers(token2),
        json={"description": "Hack"},
    )
    assert res.status_code == 403

    res = client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers(token2),
    )
    assert res.status_code == 403

    res = client.patch(
        f"/tasks/{task_id}",
        headers=auth_headers(token1),
        json={"description": "Updated"},
    )
    assert res.status_code == 200

    res = client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers(token1),
    )
    assert res.status_code == 204


def test_tasks_require_auth(client):
    res = client.get("/tasks/")
    assert res.status_code in (401, 403)

    res = client.post("/tasks/", json={"description": "x", "comment": "y"})
    assert res.status_code in (401, 403)
